from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.files.images import ImageFile
import os
from types import SimpleNamespace
from unittest.mock import patch
from io import BytesIO
import inspect
from django.test import SimpleTestCase
from django.core.handlers.wsgi import WSGIHandler
from Off_Axis_Django.asgi import application as asgi_application
from Off_Axis_Django.wsgi import application as wsgi_application
from Off_Axis_App.models import (
    Artist,
    Client,
    User,
    Gig,
    Venue,
    GenreTag,
    Address,
    Festival,
    CMS,
    Credit,
    CreditTransaction,
    Cart,
    Ticket,
)
from populate_db import populate
from Off_Axis_App.helpers.cart import get_or_create_cart
from Off_Axis_App.helpers.stripe_webhook import handle_checkout_session_completed


class HandleCheckoutSessionCompletedTestCase(TestCase):
    def setUp(self):
        # Create a user with a Client record.
        self.user = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="password",  # nosec
        )
        self.client_obj = Client.objects.create(user=self.user)

        # Create a dummy artist for the gig.
        self.artist = Artist.objects.create(
            user=User.objects.create_user(
                username="artist_for_gig", password="password"
            ),  # nosec
            bio="Test artist",
            is_approved=True,
            credit=Credit.objects.create(balance=100),
        )

        # Create a Venue
        self.venue = Venue.objects.create(
            name="Test Venue",
            address=Address.objects.create(
                line_1="123 Main St",
                city="Test City",
                country="Test Country",
                post_code="12345",
            ),
            description="Test venue description",
        )

        # Create a Gig with the required fields (including a valid artist, date, capacity, and venue).
        self.gig = Gig.objects.create(
            artist=self.artist,
            venue=self.venue,  # Add the venue here
            stripe_product_id="prod_123",
            price=10.0,
            date=timezone.now(),  # Use timezone-aware datetime
            capacity=100,
        )

    @patch("Off_Axis_App.helpers.stripe_webhook.send_ticket_email")
    @patch("Off_Axis_App.helpers.stripe_webhook.stripe.checkout.Session.retrieve")
    @patch(
        "Off_Axis_App.helpers.stripe_webhook.stripe.checkout.Session.list_line_items"
    )
    def test_handle_checkout_session_completed_success(
        self, mock_list_line_items, mock_retrieve, mock_send_ticket_email
    ):
        """
        Test a successful checkout event where the user, client, and gig exist.
        Two tickets should be created (as per quantity) and emails sent.
        """
        # Create dummy line item data.
        dummy_line_item_price = SimpleNamespace(
            product="prod_123", unit_amount_decimal="1000"
        )
        dummy_line_item = SimpleNamespace(price=dummy_line_item_price, quantity=2)
        dummy_list = SimpleNamespace(data=[dummy_line_item])
        mock_list_line_items.return_value = dummy_list

        # Create dummy breakdown with one discount.
        dummy_discount = SimpleNamespace(
            discount=SimpleNamespace(coupon=SimpleNamespace(name="DISCOUNT10"))
        )
        dummy_breakdown = SimpleNamespace(discounts=[dummy_discount])
        dummy_retrieve_response = SimpleNamespace(
            total_details=SimpleNamespace(breakdown=dummy_breakdown)
        )
        mock_retrieve.return_value = dummy_retrieve_response

        # Create a dummy checkout session.
        dummy_address = SimpleNamespace(postal_code="12345", country="US")
        dummy_customer_details = SimpleNamespace(
            email="customer@example.com", name="John Doe", address=dummy_address
        )
        dummy_checkout_session = SimpleNamespace(
            id="cs_test_123",
            customer_email="",  # email taken from customer_details below
            customer_details=dummy_customer_details,
        )
        dummy_event = SimpleNamespace(
            data=SimpleNamespace(object=dummy_checkout_session)
        )

        # Call the webhook handler.
        handle_checkout_session_completed(dummy_event)

        # Two tickets should have been created (quantity=2).
        self.assertEqual(Ticket.objects.count(), 2)
        ticket = Ticket.objects.first()
        # Verify that the purchase price is computed as 1000 / 100 = 10.0.
        self.assertEqual(ticket.purchase_price, 10.0)
        # The discount used is a comma-joined string of coupon names.
        self.assertEqual(ticket.discount_used, "DISCOUNT10")
        self.assertEqual(ticket.checkout_email, "customer@example.com")
        self.assertEqual(ticket.checkout_name, "John Doe")
        self.assertEqual(ticket.checkout_postcode, "12345")
        self.assertEqual(ticket.checkout_country, "US")
        # Ensure that the email-sending function was called twice.
        self.assertEqual(mock_send_ticket_email.call_count, 2)

    @patch("Off_Axis_App.helpers.stripe_webhook.send_ticket_email")
    @patch("Off_Axis_App.helpers.stripe_webhook.stripe.checkout.Session.retrieve")
    @patch(
        "Off_Axis_App.helpers.stripe_webhook.stripe.checkout.Session.list_line_items"
    )
    def test_handle_checkout_session_completed_no_user(
        self, mock_list_line_items, mock_retrieve, mock_send_ticket_email
    ):
        """
        Test that if no user is found for the provided email, tickets are still created
        with the user field left as None.
        """
        # Use the same dummy line item setup.
        dummy_line_item_price = SimpleNamespace(
            product="prod_123", unit_amount_decimal="1000"
        )
        dummy_line_item = SimpleNamespace(price=dummy_line_item_price, quantity=1)
        dummy_list = SimpleNamespace(data=[dummy_line_item])
        mock_list_line_items.return_value = dummy_list

        dummy_discount = SimpleNamespace(
            discount=SimpleNamespace(coupon=SimpleNamespace(name="DISCOUNT10"))
        )
        dummy_breakdown = SimpleNamespace(discounts=[dummy_discount])
        dummy_retrieve_response = SimpleNamespace(
            total_details=SimpleNamespace(breakdown=dummy_breakdown)
        )
        mock_retrieve.return_value = dummy_retrieve_response

        dummy_address = SimpleNamespace(postal_code="12345", country="US")
        dummy_customer_details = SimpleNamespace(
            email="nonexistent@example.com", name="Jane Doe", address=dummy_address
        )
        dummy_checkout_session = SimpleNamespace(
            id="cs_test_456",
            customer_email="",  # email taken from customer_details below
            customer_details=dummy_customer_details,
        )
        dummy_event = SimpleNamespace(
            data=SimpleNamespace(object=dummy_checkout_session)
        )

        handle_checkout_session_completed(dummy_event)

        # Since there is no user with this email, a ticket is created with user = None.
        self.assertEqual(Ticket.objects.count(), 1)
        ticket = Ticket.objects.first()
        self.assertIsNone(ticket.user)
        self.assertEqual(ticket.checkout_email, "nonexistent@example.com")
        self.assertEqual(ticket.checkout_name, "Jane Doe")
        self.assertEqual(mock_send_ticket_email.call_count, 1)

    @patch("Off_Axis_App.helpers.stripe_webhook.send_ticket_email")
    @patch("Off_Axis_App.helpers.stripe_webhook.stripe.checkout.Session.retrieve")
    @patch(
        "Off_Axis_App.helpers.stripe_webhook.stripe.checkout.Session.list_line_items"
    )
    def test_handle_checkout_session_completed_no_gig(
        self, mock_list_line_items, mock_retrieve, mock_send_ticket_email
    ):
        """
        Test that if no Gig is found matching the product ID from a line item,
        no Ticket is created and the email is not sent.
        """
        # Use a product ID that does not match any existing Gig.
        dummy_line_item_price = SimpleNamespace(
            product="nonexistent_prod", unit_amount_decimal="1000"
        )
        dummy_line_item = SimpleNamespace(price=dummy_line_item_price, quantity=1)
        dummy_list = SimpleNamespace(data=[dummy_line_item])
        mock_list_line_items.return_value = dummy_list

        dummy_discount = SimpleNamespace(
            discount=SimpleNamespace(coupon=SimpleNamespace(name="DISCOUNT10"))
        )
        dummy_breakdown = SimpleNamespace(discounts=[dummy_discount])
        dummy_retrieve_response = SimpleNamespace(
            total_details=SimpleNamespace(breakdown=dummy_breakdown)
        )
        mock_retrieve.return_value = dummy_retrieve_response

        dummy_address = SimpleNamespace(postal_code="12345", country="US")
        dummy_customer_details = SimpleNamespace(
            email="customer@example.com", name="John Doe", address=dummy_address
        )
        dummy_checkout_session = SimpleNamespace(
            id="cs_test_789",
            customer_email="",  # email taken from customer_details below
            customer_details=dummy_customer_details,
        )
        dummy_event = SimpleNamespace(
            data=SimpleNamespace(object=dummy_checkout_session)
        )

        handle_checkout_session_completed(dummy_event)

        # No Gig is found so no Ticket should be created.
        self.assertEqual(Ticket.objects.count(), 0)
        # The email sending function should not be called.
        self.assertEqual(mock_send_ticket_email.call_count, 0)


class GetOrCreateCartTestCase(TestCase):
    def setUp(self):
        # Clean up any existing carts.
        Cart.objects.all().delete()
        # Create a user and associated Client.
        self.user_client = User.objects.create_user(
            username="clientuser", password="test123"
        )  # nosec
        # Assume that Client has a OneToOne relation with User and a "cart" field.
        self.client_obj = Client.objects.create(user=self.user_client, cart=None)

        # Create a user and associated Artist.
        self.user_artist = User.objects.create_user(
            username="artistuser", password="test123"
        )  # nosec
        # Assume that Artist has a OneToOne relation with User and a "cart" field.
        self.artist_obj = Artist.objects.create(user=self.user_artist, cart=None)

        # Create a user without any role (no client or artist).
        self.user_no_role = User.objects.create_user(
            username="noroleuser", password="test123"
        )  # nosec

    def test_no_user_no_cartid(self):
        """When neither a user nor a cart_id is provided, a new cart is created."""
        cart = get_or_create_cart()
        self.assertIsNotNone(cart)
        self.assertEqual(Cart.objects.count(), 1)

    def test_user_no_existing_cart_client(self):
        """For a client user with no existing cart, a new cart is created and assigned."""
        cart = get_or_create_cart(u=self.user_client)
        self.assertIsNotNone(cart)
        self.client_obj.refresh_from_db()
        self.assertEqual(self.client_obj.cart, cart)
        self.assertEqual(Cart.objects.count(), 1)

    def test_user_existing_cart_client(self):
        """For a client user with an existing cart, the existing cart is returned."""
        existing_cart = Cart.objects.create()
        self.client_obj.cart = existing_cart
        self.client_obj.save()
        cart = get_or_create_cart(u=self.user_client)
        self.assertEqual(cart, existing_cart)
        self.assertEqual(Cart.objects.count(), 1)

    def test_user_no_existing_cart_artist(self):
        """For an artist user with no existing cart, a new cart is created and assigned."""
        cart = get_or_create_cart(u=self.user_artist)
        self.assertIsNotNone(cart)
        self.artist_obj.refresh_from_db()
        self.assertEqual(self.artist_obj.cart, cart)
        self.assertEqual(Cart.objects.count(), 1)

    def test_user_existing_cart_artist(self):
        """For an artist user with an existing cart, the existing cart is returned."""
        existing_cart = Cart.objects.create()
        self.artist_obj.cart = existing_cart
        self.artist_obj.save()
        cart = get_or_create_cart(u=self.user_artist)
        self.assertEqual(cart, existing_cart)
        self.assertEqual(Cart.objects.count(), 1)

    def test_cart_id_existing_valid_client(self):
        """
        When a valid cart_id is provided and the cart belongs to the user,
        the cart is returned.
        """
        cart_obj = Cart.objects.create()
        self.client_obj.cart = cart_obj
        self.client_obj.save()
        cart = get_or_create_cart(u=self.user_client, cart_id=cart_obj.id)
        self.assertEqual(cart, cart_obj)

    def test_cart_id_existing_invalid_owner(self):
        """
        When a valid cart_id is provided but belongs to a different user,
        it is ignored and a new cart is created and assigned to the provided user.
        """
        # Create a cart and assign it to the client user.
        other_cart = Cart.objects.create()
        self.client_obj.cart = other_cart
        self.client_obj.save()
        # Now, call with the artist user and the same cart_id.
        cart = get_or_create_cart(u=self.user_artist, cart_id=other_cart.id)
        self.artist_obj.refresh_from_db()
        self.assertNotEqual(cart, other_cart)
        self.assertEqual(self.artist_obj.cart, cart)
        # Two carts should exist now.
        self.assertEqual(Cart.objects.count(), 2)

    def test_cart_id_does_not_exist(self):
        """
        When a cart_id is provided that does not exist,
        a new cart is created.
        """
        cart = get_or_create_cart(cart_id=9999)
        self.assertIsNotNone(cart)
        self.assertEqual(Cart.objects.count(), 1)

    def test_cart_id_does_not_exist_with_user(self):
        """
        When a non-existent cart_id is provided along with a user,
        a new cart is created and assigned to the user.
        """
        cart = get_or_create_cart(u=self.user_client, cart_id=9999)
        self.assertIsNotNone(cart)
        self.client_obj.refresh_from_db()
        self.assertEqual(self.client_obj.cart, cart)
        self.assertEqual(Cart.objects.count(), 1)

    def test_user_without_artist_or_client(self):
        """
        If the user doesn't have associated artist or client attributes,
        a ValueError should be raised.
        """
        with self.assertRaises(ValueError):
            get_or_create_cart(u=self.user_no_role)


class PopulateDBTestCase(TestCase):
    def setUp(self):
        # Run the population script to seed the database.
        populate()

    def test_users_count(self):
        """
        Expecting:
         - 8 users created via add_artist (including admin)
         - 4 users created via add_client
         Total: 12 users.
        """
        self.assertEqual(User.objects.count(), 12, "There should be 12 users created.")

    def test_artists_count(self):
        # 8 artists should be created.
        self.assertEqual(
            Artist.objects.count(), 8, "There should be 8 artists created."
        )

    def test_clients_count(self):
        # A client is created for admin in the if block plus 4 more via add_client.
        self.assertEqual(
            Client.objects.count(), 5, "There should be 5 clients created."
        )

    def test_venues_count(self):
        # Two venues are added.
        self.assertEqual(Venue.objects.count(), 2, "There should be 2 venues created.")

    def test_gigs_count(self):
        # After deleting old gigs, the script creates 7 gigs.
        self.assertEqual(Gig.objects.count(), 7, "There should be 7 gigs created.")

    def test_genre_tags_count(self):
        # The script adds 10 genre tags.
        self.assertEqual(
            GenreTag.objects.count(), 10, "There should be 10 genre tags created."
        )

    def test_cms_created(self):
        # One CMS object should be created, and it should have 3 gigs in both just announced and featured.
        cms_objs = CMS.objects.all()
        self.assertEqual(cms_objs.count(), 1, "There should be 1 CMS created.")
        cms = cms_objs.first()
        self.assertEqual(
            cms.just_announced_gigs.count(),
            3,
            "CMS should have 3 just announced gigs.",
        )
        self.assertEqual(
            cms.featured_gigs.count(),
            3,
            "CMS should have 3 featured gigs.",
        )

    def test_festivals_count(self):
        # Three festivals should be created.
        self.assertEqual(
            Festival.objects.count(), 3, "There should be 3 festivals created."
        )

    def test_addresses_count(self):
        # Each call to add_venue creates a new Address; with 2 venues, expect 2 addresses.
        self.assertEqual(
            Address.objects.count(),
            2,
            "There should be 2 addresses created for venues.",
        )

    def test_admin_is_superuser(self):
        # Check that the admin user is created as a superuser.
        admin_user = User.objects.get(username="admin")
        self.assertTrue(admin_user.is_superuser, "Admin user should be a superuser.")

    def test_artists_have_credits(self):
        # Each artist should have an associated credit record.
        for artist in Artist.objects.all():
            self.assertIsNotNone(
                artist.credit,
                f"Artist '{artist}' should have an associated credit record.",
            )


class ASGIConfigTestCase(SimpleTestCase):
    def test_asgi_application_loaded(self):
        """Ensure the ASGI application is loaded (not None)."""
        self.assertIsNotNone(asgi_application, "ASGI application should be loaded.")

    def test_asgi_application_callable(self):
        """Ensure the ASGI application is callable."""
        self.assertTrue(
            callable(asgi_application), "ASGI application should be callable."
        )

    def test_asgi_application_is_async(self):
        """Ensure the ASGI application's __call__ method is asynchronous."""
        self.assertTrue(
            inspect.iscoroutinefunction(asgi_application.__call__),
            "ASGI application's __call__ should be asynchronous.",
        )


class WSGIConfigTestCase(SimpleTestCase):
    def test_wsgi_application_loaded(self):
        """Ensure the WSGI application is loaded (not None)."""
        self.assertIsNotNone(wsgi_application, "WSGI application should be loaded.")

    def test_wsgi_application_callable(self):
        """Ensure the WSGI application is callable."""
        self.assertTrue(
            callable(wsgi_application), "WSGI application should be callable."
        )

    def test_wsgi_application_instance(self):
        """Ensure the WSGI application is an instance of Django's WSGIHandler."""
        self.assertIsInstance(
            wsgi_application,
            WSGIHandler,
            "WSGI application should be an instance of django.core.handlers.wsgi.WSGIHandler.",
        )


def init_artists_cms(self):
    # Create two artists
    self.user1 = User.objects.create_user(
        username="artist1", password="test123"
    )  # nosec
    self.user2 = User.objects.create_user(
        username="artist2", password="test123"
    )  # nosec

    with open("./static/images/gig-placeholder.png", "rb") as f:
        self.artist1 = Artist.objects.create(
            user=self.user1,
            bio="Test bio",
            is_approved=True,
            profile_picture=ImageFile(f),
            credit=Credit.objects.create(balance=2.00),
        )

        self.artist2 = Artist.objects.create(
            user=self.user2,
            bio="Test bio",
            is_approved=True,
            profile_picture=ImageFile(f),
            credit=Credit.objects.create(balance=2.00),
        )

    # Initialize credits
    self.artist1.credit.balance = 100
    self.artist1.credit.save()
    self.artist2.credit.balance = 10
    self.artist2.credit.save()

    self.address = Address.objects.create(
        line_1="123 Main St",
        line_2="Suite 1",
        country="TestCountry",
        city="TestCity",
        state_or_province="TestState",
        post_code="12345",
    )
    self.venue = Venue.objects.create(
        name="Test Venue",
        address=self.address,
        description="Test venue description",
    )
    # Create a Gig for artist2
    self.gig = Gig.objects.create(
        artist=self.artist2,
        venue=self.venue,
        date=timezone.now(),
        price=50.00,
        booking_fee=5.00,
        capacity=100,
        description="Test gig",
    )

    with open("./static/images/gig-placeholder.png", "rb") as f:
        self.gig.gig_picture.save("gig-placeholder.png", ImageFile(f), save=True)

    cms = CMS.objects.create()
    gigs = Gig.objects.all()
    cms.just_announced_gigs.add(*gigs)
    cms.featured_gigs.add(*gigs)
    cms.artist_of_the_week = self.artist1
    cms.save()


class CreditTransactionTestCase(TestCase):
    def setUp(self):
        init_artists_cms(self)

    def test_support_artist_success(self):
        """Test a successful support request."""
        self.client.login(username="artist1", password="test123")  # nosec
        initial_balance = self.artist1.credit.balance
        support_amount = 20
        response = self.client.post(
            reverse("support_artist_gig", args=[self.gig.id]),
            data={"amount": str(support_amount)},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        # Refresh the credit object to get the updated balance.
        self.artist1.credit.refresh_from_db()
        self.assertEqual(self.artist1.credit.balance, initial_balance - support_amount)

    def test_accept_support(self):
        # Create a pending transaction from artist1 to artist2
        transaction = CreditTransaction.objects.create(
            from_artist=self.artist1, to_artist=self.artist2, amount=20
        )
        # Log in as artist2 (the recipient)
        self.client.login(username="artist2", password="test123")  # nosec

        # Call the accept_support view
        response = self.client.post(reverse("accept_support", args=[transaction.id]))
        self.assertEqual(response.status_code, 200)

        # Refresh objects to get updated values
        transaction.refresh_from_db()
        self.artist1.credit.refresh_from_db()
        self.artist2.credit.refresh_from_db()

        # Check that the transaction status is updated and balances are adjusted
        self.assertEqual(transaction.status, "accepted")
        self.assertEqual(self.artist1.credit.balance, 100)
        self.assertEqual(self.artist2.credit.balance, 30)  # 10 + 20

    def test_reject_support(self):
        """Test that rejecting a support transaction refunds the supporter and deletes the transaction."""
        self.client.login(username="artist1", password="test123")  # nosec
        support_amount = 20
        initial_balance = self.artist1.credit.balance
        response = self.client.post(
            reverse("support_artist_gig", args=[self.gig.id]),
            data={"amount": str(support_amount)},
        )
        self.assertEqual(response.status_code, 200)
        # The transaction should have been created with a 'pending' status.
        transaction = CreditTransaction.objects.get(
            from_artist=self.artist1, to_artist=self.artist2, gig=self.gig
        )
        self.assertEqual(transaction.status, "pending")
        self.artist1.credit.refresh_from_db()
        self.assertEqual(self.artist1.credit.balance, initial_balance - support_amount)

        # Now, artist2 rejects the support request.
        self.client.logout()
        self.client.login(username="artist2", password="test123")  # nosec
        response = self.client.post(reverse("reject_support", args=[transaction.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Artist1's credit should have been refunded.
        self.artist1.credit.refresh_from_db()
        self.assertEqual(self.artist1.credit.balance, initial_balance)

        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "Transaction rejected")
        # The transaction should no longer exist.
        with self.assertRaises(CreditTransaction.DoesNotExist):
            CreditTransaction.objects.get(id=transaction.id)

    def test_support_artist_missing_amount(self):
        """
        Test that the support_artist_gig view returns an error when the 'amount'
        field is missing from the POST data.
        """
        # Log in as artist1 (the supporter)
        self.client.login(username="artist1", password="test123")  # nosec
        # Post without 'amount'
        response = self.client.post(
            reverse("support_artist_gig", args=[self.gig.id]), data={}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Invalid request")

    def test_support_artist_non_numeric_amount(self):
        """
        Test that the support_artist_gig view returns an error when the 'amount'
        field is not a valid number.
        """
        self.client.login(username="artist1", password="test123")  # nosec
        # Post with a non-numeric amount
        response = self.client.post(
            reverse("support_artist_gig", args=[self.gig.id]), data={"amount": "abc"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Invalid amount")

    def test_support_artist_insufficient_credit(self):
        """
        Test that the support_artist_gig view returns an error when the sender (from_artist)
        does not have enough credits to support the recipient.
        """
        # Set artist1's credit balance lower than the support amount
        self.artist1.credit.balance = 5
        self.artist1.credit.save()

        self.client.login(username="artist1", password="test123")  # nosec
        # Attempt to support with an amount greater than the available credits
        response = self.client.post(
            reverse("support_artist_gig", args=[self.gig.id]), data={"amount": "20"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Not enough credits to send")


class AuthenticationTestCase(TestCase):
    def setUp(self):
        # Create a user for testing login and password reset
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = "Password123!"  # nosec
        self.user = User.objects.create_user(
            username=self.username, email=self.email, password=self.password
        )

        init_artists_cms(self)

    # --- Login Tests ---
    def test_login_success(self):
        # Post valid credentials to the login view
        response = self.client.post(
            reverse("login"),
            data={
                "username": self.username,
                "password": self.password,
            },
        )
        # Django's login view redirects on success (status 302)
        self.assertEqual(response.status_code, 302)
        # Ensure that the user is authenticated in a subsequent request
        response = self.client.get(reverse("index"))
        self.assertTrue(response.context["user"].is_authenticated)

    def test_login_failure_invalid_password(self):
        response = self.client.post(
            reverse("login"),
            data={
                "username": self.username,
                "password": "WrongPassword",
            },
        )
        # The page should reload with errors (status 200)
        self.assertEqual(response.status_code, 200)
        # Check that the error message is displayed (default Django message)
        self.assertContains(response, "Please enter a correct username and password")
        response = self.client.get(reverse("index"))
        self.assertFalse(response.context["user"].is_authenticated)

    def test_login_failure_nonexistent_user(self):
        response = self.client.post(
            reverse("login"),
            data={
                "username": "nonexistent",
                "password": "AnyPassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password")
        response = self.client.get(reverse("index"))
        self.assertFalse(response.context["user"].is_authenticated)

    # --- Password Reset Tests ---
    def test_password_reset_view_get(self):
        # Ensure that the password reset page loads correctly via GET
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reset Password")

    def test_password_reset_invalid_email(self):
        # Posting an email that does not exist should still redirect (security reasons)
        response = self.client.post(
            reverse("password_reset"), data={"email": "nonexistent@example.com"}
        )
        self.assertEqual(response.status_code, 302)
        # No email should be sent if the email is not associated with a user
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_valid_email(self):
        # Submitting a valid email should send an email
        response = self.client.post(
            reverse("password_reset"), data={"email": self.email}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        # Check that the email body contains a reset link
        self.assertIn("Reset your password", mail.outbox[0].body)

    def test_password_reset_confirm_invalid_token(self):
        # Test the password reset confirmation view with an invalid uid/token combination.
        uidb64 = "invaliduid"
        token = "invalid-token"  # nosec
        url = reverse(
            "password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The password reset link was invalid")

    def test_password_reset_confirm_valid(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})

        # First GET returns a redirect with token replaced
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        redirect_url = response["Location"]

        # Get the final form page
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter new password")

        # Post the new password via POST to the redirect URL
        new_password = "NewPassword123!"  # nosec
        response = self.client.post(
            redirect_url,
            data={"new_password1": new_password, "new_password2": new_password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        # Verify that the user can log in with the new password
        self.client.logout()
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

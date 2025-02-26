# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User
# from .models import Artist, Credit, CreditTransaction, Venue, Gig, Address
# from django.utils import timezone
# from django.core import mail
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator

# # Register your models here.
# # admin.site.register(Artist)
# # admin.site.register(Client)
# # admin.site.register(SocialLink)
# # admin.site.register(GenreTag)


# class CreditTransactionTestCase(TestCase):
#     def setUp(self):
#         # Create two artists
#         self.user1 = User.objects.create_user(username="artist1", password="test123")
#         self.artist1 = Artist.objects.create(user=self.user1)
#         self.user2 = User.objects.create_user(username="artist2", password="test123")
#         self.artist2 = Artist.objects.create(user=self.user2)

#         # Initialize credits
#         self.artist1.credit.balance = 100
#         self.artist1.credit.save()
#         self.artist2.credit.balance = 10
#         self.artist2.credit.save()

#         self.address = Address.objects.create(
#             line_1="123 Main St",
#             line_2="Suite 1",
#             country="TestCountry",
#             city="TestCity",
#             state_or_province="TestState",
#             post_code="12345",
#         )
#         self.venue = Venue.objects.create(
#             name="Test Venue",
#             address=self.address,
#             description="Test venue description",
#             venue_photo_url="http://example.com/venue.jpg",
#         )
#         # Create a Gig for artist2
#         self.gig = Gig.objects.create(
#             artist=self.artist2,
#             venue=self.venue,
#             date=timezone.now(),
#             price=50.00,
#             booking_fee=5.00,
#             capacity=100,
#             description="Test gig",
#             gig_photo_url="http://example.com/gig.jpg",
#         )

#     def test_accept_support(self):
#         # Create a pending transaction from artist1 to artist2
#         transaction = CreditTransaction.objects.create(
#             from_artist=self.artist1, to_artist=self.artist2, amount=20
#         )
#         # Log in as artist2 (the recipient)
#         self.client.login(username="artist2", password="test123")

#         # Call the accept_support view
#         response = self.client.post(reverse("accept_support", args=[transaction.id]))
#         self.assertEqual(response.status_code, 200)

#         # Refresh objects to get updated values
#         transaction.refresh_from_db()
#         self.artist1.credit.refresh_from_db()
#         self.artist2.credit.refresh_from_db()

#         # Check that the transaction status is updated and balances are adjusted
#         self.assertEqual(transaction.status, "accepted")
#         self.assertEqual(self.artist1.credit.balance, 80)  # 100 - 20
#         self.assertEqual(self.artist2.credit.balance, 30)  # 10 + 20

#     def test_reject_support(self):
#         # Create a pending transaction from artist1 to artist2
#         transaction = CreditTransaction.objects.create(
#             from_artist=self.artist1, to_artist=self.artist2, amount=20
#         )
#         # Log in as artist2 (the recipient)
#         self.client.login(username="artist2", password="test123")

#         # Call the reject_support view (assuming it reverses or deletes the transaction)
#         response = self.client.post(reverse("reject_support", args=[transaction.id]))
#         self.assertEqual(response.status_code, 200)

#         # Verify that the transaction has been deleted or marked rejected as per your logic
#         with self.assertRaises(CreditTransaction.DoesNotExist):
#             CreditTransaction.objects.get(id=transaction.id)

#     def test_support_artist_missing_amount(self):
#         """
#         Test that the support_artist_gig view returns an error when the 'amount'
#         field is missing from the POST data.
#         """
#         # Log in as artist1 (the supporter)
#         self.client.login(username="artist1", password="test123")
#         # Post without 'amount'
#         response = self.client.post(
#             reverse("support_artist_gig", args=[self.gig.id]), data={}
#         )
#         self.assertEqual(response.status_code, 400)
#         self.assertIn("error", response.json())
#         self.assertEqual(response.json()["error"], "Invalid request")

#     def test_support_artist_non_numeric_amount(self):
#         """
#         Test that the support_artist_gig view returns an error when the 'amount'
#         field is not a valid number.
#         """
#         self.client.login(username="artist1", password="test123")
#         # Post with a non-numeric amount
#         response = self.client.post(
#             reverse("support_artist_gig", args=[self.gig.id]), data={"amount": "abc"}
#         )
#         self.assertEqual(response.status_code, 400)
#         self.assertIn("error", response.json())
#         self.assertEqual(response.json()["error"], "Invalid amount")

#     def test_support_artist_insufficient_credit(self):
#         """
#         Test that the support_artist_gig view returns an error when the sender (from_artist)
#         does not have enough credits to support the recipient.
#         """
#         # Set artist1's credit balance lower than the support amount
#         self.artist1.credit.balance = 5
#         self.artist1.credit.save()

#         self.client.login(username="artist1", password="test123")
#         # Attempt to support with an amount greater than the available credits
#         response = self.client.post(
#             reverse("support_artist_gig", args=[self.gig.id]), data={"amount": "20"}
#         )
#         self.assertEqual(response.status_code, 400)
#         self.assertIn("error", response.json())
#         self.assertEqual(response.json()["error"], "Not enough credits to send")


# class AuthenticationTestCase(TestCase):
#     def setUp(self):
#         # Create a user for testing login and password reset
#         self.username = "testuser"
#         self.email = "testuser@example.com"
#         self.password = "Password123!"
#         self.user = User.objects.create_user(
#             username=self.username, email=self.email, password=self.password
#         )

#     # --- Login Tests ---
#     def test_login_success(self):
#         # Post valid credentials to the login view
#         response = self.client.post(
#             reverse("login"),
#             data={
#                 "username": self.username,
#                 "password": self.password,
#             },
#         )
#         # Django's login view redirects on success (status 302)
#         self.assertEqual(response.status_code, 302)
#         # Ensure that the user is authenticated in a subsequent request
#         response = self.client.get(reverse("index"))
#         self.assertTrue(response.context["user"].is_authenticated)

#     def test_login_failure_invalid_password(self):
#         response = self.client.post(
#             reverse("login"),
#             data={
#                 "username": self.username,
#                 "password": "WrongPassword",
#             },
#         )
#         # The page should reload with errors (status 200)
#         self.assertEqual(response.status_code, 200)
#         # Check that the error message is displayed (default Django message)
#         self.assertContains(response, "Please enter a correct username and password")
#         response = self.client.get(reverse("index"))
#         self.assertFalse(response.context["user"].is_authenticated)

#     def test_login_failure_nonexistent_user(self):
#         response = self.client.post(
#             reverse("login"),
#             data={
#                 "username": "nonexistent",
#                 "password": "AnyPassword",
#             },
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Please enter a correct username and password")
#         response = self.client.get(reverse("index"))
#         self.assertFalse(response.context["user"].is_authenticated)

#     # --- Password Reset Tests ---
#     def test_password_reset_view_get(self):
#         # Ensure that the password reset page loads correctly via GET
#         response = self.client.get(reverse("password_reset"))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Reset Password")

#     def test_password_reset_invalid_email(self):
#         # Posting an email that does not exist should still redirect (security reasons)
#         response = self.client.post(
#             reverse("password_reset"), data={"email": "nonexistent@example.com"}
#         )
#         self.assertEqual(response.status_code, 302)
#         # No email should be sent if the email is not associated with a user
#         self.assertEqual(len(mail.outbox), 0)

#     def test_password_reset_valid_email(self):
#         # Submitting a valid email should send an email
#         response = self.client.post(
#             reverse("password_reset"), data={"email": self.email}
#         )
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(len(mail.outbox), 1)
#         # Check that the email body contains a reset link
#         self.assertIn("Reset your password", mail.outbox[0].body)

#     def test_password_reset_confirm_invalid_token(self):
#         # Test the password reset confirmation view with an invalid uid/token combination.
#         uidb64 = "invaliduid"
#         token = "invalid-token"
#         url = reverse(
#             "password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}
#         )
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "The password reset link was invalid")

#     def test_password_reset_confirm_valid(self):
#         uid = urlsafe_base64_encode(force_bytes(self.user.pk))
#         token = default_token_generator.make_token(self.user)
#         url = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
#         # Follow redirects to reach the final page with the reset form
#         response = self.client.get(url, follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Enter new password")

#         # Submit the new password via POST
#         new_password = "NewPassword456!"
#         response = self.client.post(
#             url,
#             data={
#                 "new_password1": new_password,
#                 "new_password2": new_password,
#             },
#             follow=True,
#         )
#         # Expect a redirect after a successful reset, and then the final page should have a status code 200
#         self.assertEqual(response.status_code, 200)
#         # Verify that the user can log in with the new password
#         self.client.logout()
#         login_response = self.client.post(
#             reverse("login"),
#             data={
#                 "username": self.username,
#                 "password": new_password,
#             },
#         )
#         self.assertEqual(login_response.status_code, 302)

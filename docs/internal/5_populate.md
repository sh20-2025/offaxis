# Population Script Documentation

## Overview
This script seeds the Off_Axis Django application's database with initial/test data. It creates admin and regular users, artists, clients, genre tags, venues, gigs, CMS content, and festivals while integrating with Stripe for gig product management.

## Setup
- **Environment:**
  Sets the `DJANGO_SETTINGS_MODULE` and initializes Django.
- **Stripe Integration:**
  Sets `stripe.api_key` from the `STRIPE_SECRET_KEY` environment variable.

## Main Functionality

### `populate()`
- **Data Cleanup:**
  Deletes all existing `Artist`, `Client`, `User`, and `Gig` objects and archives existing Stripe products.
- **Admin Creation:**
  Checks for an admin user; if not present, creates one along with an associated client and artist record.
- **Genre Tags:**
  Creates a list of genre tags (e.g., Rock, Pop, Rap, etc.).
- **Artists & Clients:**
  Creates multiple artist records (approved and unapproved) via `add_artist` and client records via `add_client`.
- **Venues & Gigs:**
  Creates venues using `add_venue` and multiple gigs via `add_gig` (approved gigs trigger Stripe product creation).
- **CMS Content:**
  Sets up a CMS record with just announced and featured gigs and assigns an artist of the week.
- **Festivals:**
  Deletes existing festivals and creates new ones via `add_festival`.

## Helper Functions

- **`add_artist(name, bio, is_approved)`**
  Creates or retrieves a user and associated artist with the given details, using a placeholder image and initializing credit.

- **`add_client(name, phone_number)`**
  Creates or retrieves a client linked to a user with the provided name and phone number.

- **`add_venue(name, description, venue_picture)`**
  Creates an Address and Venue with static address details and the given parameters.

- **`add_gig(artist, venue, date, price, capacity, description, is_approved=True)`**
  Creates or retrieves a gig with the provided details; if approved, calls `g.approve()` to set up the Stripe product.

- **`add_genre_tag(tag)`**
  Creates or retrieves a genre tag by name.

- **`add_festival(name, description, start_date, end_date, artists, festival_photo_url, youtube_video_url)`**
  Creates or retrieves a festival with the given details and associates it with a list of artists.

## Execution
When run directly, the script prints "Populating database..." and calls the `populate()` function to seed the database.

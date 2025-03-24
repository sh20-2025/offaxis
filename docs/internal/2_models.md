
# Models Documentation

## Client
- Linked one-to-one with a Django user.
- Stores billing info, phone number, and an associated cart.

## Artist
- One-to-one with a Django user; stores bio, approval status, profile picture, social links, genre tags, slug, and credit.
- Auto-generates slug; initializes credit on save.

## SocialLink
- Represents a social media link with a type (Spotify, YouTube, SoundCloud, Instagram, WhatsApp) and URL.

## GenreTag
- Represents a musical genre tag.

## ContactInformation
- Captures contact form submissions (names, email, message, message type).

## Gig
- Represents an event, linked to an artist and venue.
- Stores event details (date, price, booking fee, capacity, description, picture, approval, Stripe product ID, closed flag).
- Provides helper methods for ticket counts, full price calculation, and approval (with Stripe product creation).

## Venue
- Represents a gig venue with a name, one-to-one address, description, and optional picture.

## Ticket
- Represents a purchased ticket linked to a gig and client.
- Stores checkout details, purchase price, discount info, usage status, QR code image/data, and creation timestamp.

## Address
- Represents a physical address (lines, city, state, country, postal code).

## Cart & CartItem
- **Cart:** A unique shopping cart identified by a UUID.
- **CartItem:** Links a gig to a cart with quantity and total price details.

## Festival
- Represents a festival event with name, description, date range, associated artists, YouTube URL, slug, active status, and photo URL.
- Auto-generates slug on save.

## Credit & CreditTransaction
- **Credit:** Tracks an artist’s credit balance.
- **CreditTransaction:** Logs support transactions between artists (amount, status [pending, accepted, rejected], timestamp, associated gig).

## CMS
- Manages homepage content with many-to-many relations to gigs (just announced, featured) and an "artist of the week."

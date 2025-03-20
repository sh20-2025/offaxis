## Members

- 2840506 Heng Zhen Yao 
- 2671747 Dulmant Jan
- 2777042 Levack Fraser Wiremu 
- 2802089 Tee Zhi Xi 
- 2618972 McIntyre Aaron
- 2768903 Nelson Freddie 

## Requirements

- python 3.12
- django 5.1.2

## Contributing

Commit messages should follow the guidelines described [here](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)

Once you have cloned the repository, you can run the `setup.ps1` script setup python and it's dependencies, as well as pre-commit hooks.

```powershell
.\scripts\setup.ps1
```

The python virtual environment will be created in `C:\Users\Public\sh20-main-venv`, it will be automatically activated by the setup script. However you can also activate it using:

```powershell
.\scripts\activate-venv.ps1
```

And deactivate it using:

```powershell
deactivate
```

All code is ran through the black formatter, and the flake8 linter by the pre-commit hooks. The pre-commit hooks will run these checks before allowing you to commit. You may also run these tools from the command line using:

```powershell
black .
```

```powershell
flake8 .
```

You are now ready to start developing!

## Models

### User Roles

#### Client

- Each Client is linked to a Django User.

- Stores cart, billing info, and phone number.

- Created automatically when a User is created.

#### Artist

- Represents an artist profile linked to a Django User.

- Has a bio, approval status, profile picture, social links, genre tags, and a slug.

- Holds credit balance and transaction history.

- Saves a unique slug from the username.

### Social and Genre Tags

#### SocialLink

- Stores social media links for artists (e.g., Spotify, YouTube, Instagram).

#### GenreTag

- Represents music genres associated with an artist.

### Contact and Communication

#### ContactInformation

- Stores user inquiries with fields like name, email, message, and message type.

### Event Management

#### Gig

- Represents a live music event.

- Stores artist, venue, date, price, capacity, and ticket sales.

- Includes approval status and Stripe product ID for payment handling.

#### Venue

- Stores venue details including name, address, description, and an image.

#### Ticket

- Represents a ticket purchase.

- Links a gig to a client with checkout details.

- Includes a QR code for validation.

### Address and Cart

#### Address

- Stores an address related to a venue.

#### Cart & CartItem

- Cart: A container for storing gig tickets before purchase.

- CartItem: Represents individual gig tickets added to a cart.

### Festivals

#### Festival

- Represents a music festival.

- Stores details like name, description, date range, artists, and media links.

- Uses a slug for URL-friendly naming.

### Credits and Transactions

#### Credit

- Represents an artist's credit balance.

- Defaults to 2 credits on creation.

#### CreditTransaction

- Represents transactions between artists.

- Has sender (from_artist), receiver (to_artist), amount, status, and a linked gig.

### CMS (Content Management System)

#### CMS

- Manages website content.

- Stores featured gigs, newly announced gigs, and an artist of the week.

Key Features

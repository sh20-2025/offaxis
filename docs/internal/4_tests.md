# Test Suite Documentation

## Common Test Data Initialization

- **`init_artists_cms(self)`**
  - Creates two artist users (`artist1` and `artist2`) with associated credits.
  - Sets up a venue, address, and a gig for `artist2`.
  - Configures a CMS instance to feature the created gig and assigns `artist1` as the artist of the week.

## Credit Transaction Tests

**Test Case: `CreditTransactionTestCase`**

- **Support Request Success**
  - Logs in as `artist1` and posts a valid support request (e.g., 20 credits).
  - Confirms that the response is successful (HTTP 200) and that `artist1`'s credit balance is reduced accordingly.

- **Accepting Support**
  - Creates a pending credit transaction from `artist1` to `artist2`.
  - Logs in as `artist2` and posts to accept the support.
  - Verifies that the transaction status is updated to "accepted" and that the credits are transferred (increasing `artist2`’s balance).

- **Rejecting Support**
  - Posts a valid support request as `artist1`, then logs in as `artist2` to reject it.
  - Checks that the transaction is deleted and that `artist1`'s credits are refunded.

- **Missing or Invalid Amount**
  - Tests that omitting the `amount` field returns an error.
  - Tests that submitting a non-numeric `amount` returns an "Invalid amount" error.

- **Insufficient Credit**
  - Adjusts `artist1`’s credit to be lower than the requested support amount.
  - Confirms that the support request fails with an error indicating insufficient credits.

## Authentication Tests

**Test Case: `AuthenticationTestCase`**

### Login Tests

- **Successful Login**
  - Submits valid credentials and verifies that the user is redirected and remains authenticated on subsequent requests.

- **Login with Invalid Password**
  - Submits an incorrect password and checks that the proper error message is shown without authenticating the user.

- **Login for Nonexistent User**
  - Attempts login with a username that does not exist and verifies that authentication fails and the error message is displayed.

### Password Reset Tests

- **Password Reset Page Load**
  - Ensures the password reset form is accessible via GET.

- **Invalid Email Submission**
  - Submits an email not linked to any account and confirms that no email is sent while still redirecting (for security).

- **Valid Email Submission**
  - Submits a valid email, checks that an email is sent, and that the reset link is included in the email content.

- **Password Reset Confirmation with Invalid Token**
  - Accesses the reset confirmation view with an invalid UID/token combination and checks for an error message about an invalid link.

- **Password Reset Confirmation Flow**
  - Generates a valid UID and token, follows the redirect to the reset form, and posts a new password.
  - Confirms that the new password is accepted and that the user can log in with it.

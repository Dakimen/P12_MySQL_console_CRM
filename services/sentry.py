import sentry_sdk

from config import DSN


class SentryJournalisation:
    """
    Class responsible for managing Sentry Journalisation
    and capture of unexpected errors.

    Includes methods used to forward to send notifications
    to the Sentry dashboard about the creation and update of collaborators,
    as well as signing of any contract.
    """
    def __init__(self):
        """
        Initialise Sentry_sdk.
        """
        sentry_sdk.init(
            dsn=DSN,
            send_default_pii=True,
        )

    def create_collaborator(self, name, email, created_by):
        """
        Captures collaborator creation information to Sentry.

        name (str): Name of the newly created collaborator.
        email (str): Email of the newly created collaborator.
        created_by (UUID): UUID of the management responsible for creation.
        """
        try:
            sentry_sdk.set_context("collaborator", {
                "name": name,
                "email": email,
                "created_by": created_by
            })
            sentry_sdk.capture_message("Collaborator created")

            return None

        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise

    def update_collaborator_email(self, name, new_email, updated_by):
        """
        Captures collaborator's email update information to Sentry.

        name (str): Name of the collaborator.
        new_email (str): Collaborator's new email.
        created_by (UUID): UUID of the management responsible for this update.
        """
        try:
            sentry_sdk.set_context("collaborator_update_email", {
                "name": name,
                "new_email": new_email,
                "updated_by": updated_by
            })
            sentry_sdk.capture_message("Collaborator email updated")

        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise

    def update_collaborator_name(self, new_name, email, updated_by):
        """
        Captures collaborator's name update information to Sentry.

        new_name (str): New name of the collaborator.
        email (str): Collaborator's email.
        created_by (UUID): UUID of the management responsible for this update.
        """
        try:
            sentry_sdk.set_context("collaborator_update_name", {
                "new_name": new_name,
                "email": email,
                "updated_by": updated_by
            })
            sentry_sdk.capture_message("Collaborator name updated")
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise

    def update_collaborator_role(self, email, new_role, updated_by):
        """
        Captures collaborator's role update information to Sentry.

        email (str): Collaborator's email.
        new_role (str): Collaborator's new role.
        created_by (UUID): UUID of the management responsible for this update.
        """
        try:
            sentry_sdk.set_context("collaborator_update_role", {
                "email": email,
                "new_role": new_role,
                "updated_by": updated_by
            })
            sentry_sdk.capture_message("Collaborator assigned role")
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise

    def sign_contract(self, client, signed, modif_by):
        """
        Captures contract's signing to Sentry.

        client (UUID): Client's UUID.
        signed (datetime): Contract's signature date.
        created_by (UUID): UUID of the management responsible for this update.
        """
        try:
            sentry_sdk.set_context("contract", {
                "client": client,
                "contract_signed_date": signed,
                "signed_data_entered_by": modif_by
            })
            sentry_sdk.capture_message("Contract signed")

        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise

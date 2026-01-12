import sentry_sdk

from config import DSN


class SentryJournalisation:
    def __init__(self):
        sentry_sdk.init(
            dsn=DSN,
            send_default_pii=True,
        )

    def create_collaborator(self, name, email, created_by):
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

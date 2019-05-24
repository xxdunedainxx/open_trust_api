# General library imports
from functools import wraps

# Token handler
from google_transfer1_0.core.util.session_and_tokens.token_authentication import TOKEN_HANDLER

# Flask imports
from flask import request

# API Util imports
from google_transfer1_0.core.util.general.basic import get_loged_in_user

# Config
from google_transfer1_0.core.conf.general.conf import GENERAL_CONFIG
from google_transfer1_0.core.util.validators.InternalAPIValidators import InternalAPIValidators

from google_transfer1_0.core.data.models.transfer import TransferRoutines
from google_transfer1_0.core.service.helpers.trigger_transfer.AD.ADHelpers import ADHelper
from google_transfer1_0.jobs.trigger_transfer.conf.AD.conf import conf as ADSvcConfig


def is_authed_token(request,transfer_id):
    # Potentially authenticate a tokenized request
    TOKEN_HANDLER.INSPECT_AUTH_HEADER(request, get_loged_in_user(False), transfer_id)

    # Ensure their session is authed
    AUTH = TOKEN_HANDLER.AUTHENTICATE_USER_REQUEST(transfer_id, get_loged_in_user(False),
                                                   f"{GENERAL_CONFIG.jwt_key_path}\\hs256.key",
                                                   f"{GENERAL_CONFIG.rsa_keys_path}\\private.key")
    return AUTH

def is_authed_ad(transfer_id):

    if TransferRoutines.get_transfer_event(id=transfer_id).email.split("@")[0] == get_loged_in_user(dev=GENERAL_CONFIG.dev_mode_enabled).split("/")[1]:
       return {'already_authed': True}
    else:
        # Use ADSvc to query
        ADSvc = ADHelper(serviceConfig=ADSvcConfig)


        return {'already_authed':
            ADSvc.is_transfer_admin(
                user=get_loged_in_user(dev=GENERAL_CONFIG.dev_mode_enabled).split("/")[1])
        }



def auth_transfer_resource(api):
    @wraps(api)
    def auth_api(*args, **kwargs):
            # NOTE :: First we validate the TID
            ValidateTransfer=InternalAPIValidators.validate_tid(tid=kwargs['transferID'])
            if ValidateTransfer[0]["ok"] is False:
                return ValidateTransfer


            AUTHENTICATE=is_authed_ad(kwargs['transferID'])
            if AUTHENTICATE['already_authed'] is False:
                return AUTHENTICATE, 306
            else:
                return api(*args,**kwargs)
    return auth_api
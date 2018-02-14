"""This file contains configuration management functionality."""
import datetime
import os


class ConfigHelper(object):
    """Retrieve configuration settings from environment variables and CLI args.

    Attributes:
        aws_key(str): AWS API key.
        aws_secret(str): AWS API secret.
        halo_api_key(str): Halo API key.
        halo_api_secret(str): Halo API secret.
        halo_api_hostname(str): Hostname for Halo API.
        halo_module(str): ``events`` or ``scans``
        application_mode(str): ``push`` or ``pop``
        sqs_queue_url(str): URL for SQS queue.
        start_time(str): Timestamp for start of query.
    """

    def __init__(self):
        """Call other methods to set instance variables."""
        # Initialize all None
        self.aws_key = None
        self.aws_secret = None
        self.halo_key = None
        self.halo_secret = None
        self.halo_api_hostname = None
        self.halo_module = None
        self.application_mode = None
        self.sqs_queue_url = None
        self.start_time = None
        # Now set according to env.
        self.set_config_vars_from_env()
        # Make sure we have everything we need.
        self.sanity_check_for_application_mode()
        return

    def sanity_check_for_application_mode(self):
        """Check that all necessary variables are set for application mode."""
        # Generally required settings
        gen_req = {"AWS SQS queue URL": self.sqs_queue_url,
                   "AWS API key": self.aws_key,
                   "AWS API secret": self.aws_secret,
                   "Application mode": self.application_mode,
                   "Halo module": self.halo_module}
        # Required only to push Halo data to SQS queue.
        push_req = {"Halo API key": self.halo_key,
                    "Halo API secret": self.halo_secret,
                    "Halo API hostname": self.halo_api_hostname,
                    "Start time": self.start_time}
        if self.application_mode not in ["push", "pop"]:
            raise ValueError("Application mode must be \"push\" or \"pop\".")
        if self.halo_module not in ["events", "scans"]:
            raise ValueError("Halo module must be \"events\" or \"scans\".")
        # Find missing settings for generall requirements
        missing_settings = [x[0] for x in gen_req if x[1] is None]
        # If we're pushing to queue, check for a few more settings.
        if self.application_mode == "push":
            missing_settings.extend([x[0] for x in push_req if x[1] is None])
        # If any required settings are missing, raise ValueError with a
        # meaningful message.
        if missing_settings:
            msg = ("Unable to initialize config.  Missing settings:" %
                   ", ".join(missing_settings))
            raise ValueError(msg)
        return

    def set_config_vars_from_env(self):
        """Set instance variables from environment variables."""
        targets = {"APPLICATION_MODE": "application_mode",
                   "AWS_ACCESS_KEY_ID": "aws_key",
                   "AWS_SECRET_ACCESS_KEY": "aws_secret",
                   "HALO_API_KEY": "halo_key",
                   "HALO_API_SECRET_KEY": "halo_secret",
                   "HALO_API_HOSTNAME": "halo_api_hostname",
                   "HALO_MODULE": "halo_module",
                   "SQS_QUEUE_URL": "sqs_queue_url"}
        for envvar, varname in targets.items():
            setattr(self, varname, os.getenv(envvar))
        return

    @classmethod
    def get_now_timestamp(cls):
        return datetime.now().isoformat()
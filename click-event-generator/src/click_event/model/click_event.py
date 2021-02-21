class ClickEvent:

    def __init__(self):
        self.user_id = None
        self.session_id  = None
        self.session_start = None
        self.session_size = None
        self.click_article_id = None
        self.click_timestamp = None
        self.click_environment = None
        self.click_device_group = None
        self.click_os = None
        self.click_country = None

    def to_dict(self):
        click_event_dict = {"user_id": self.user_id,
                            "session_id": self.session_id,
                            "session_start": self.session_start,
                            "click_article_id": self.click_article_id,
                            "click_timestamp": self.click_timestamp,
                            "click_environment": self.click_environment,
                            "click_device_group": self.click_device_group,
                            "click_os": self.click_os,
                            "click_country": self.click_country}
        return click_event_dict






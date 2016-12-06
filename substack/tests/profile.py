from substack_core.data.profile import Profile


profile = Profile()

# profile.set_target("bkav.com, garena.com")

profile.set_enabled_plugins('search', ['BingEngine', 'BaiduEngine'])

http_settings = {
    "agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "proxy": ""
}

misc_settings = {
    "max_discovery_time": 300,
    "silent": False,
    "log_path": "D:/Everping/Work/Projects/substack/log/substack.log",
}

profile.set_http_settings(http_settings)
profile.set_misc_settings(misc_settings)
profile.set_name("empty_profile")
profile.set_desc("This is an empty profile that you can use to start a new configuration from.")

profile.save("empty")
#
# a = Profile("empty")
# print a.get_misc_settings()
# print a.get_http_settings("agent")

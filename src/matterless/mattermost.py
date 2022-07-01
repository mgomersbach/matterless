import mattermostdriver
import datastore
from shelved_cache.keys import autotuple_hashkey
from shelved_cache import cachedasyncmethod
from cachetools import cachedmethod


class MattermostManager:
    def __init__(self, options) -> None:
        """Initialize."""
        self.cache = datastore.cache
        self.driver = mattermostdriver.Driver(options)
        self.driver.login()

    @property
    # @cachedmethod(lambda self: self.cache["my_user"], key=autotuple_hashkey)
    def my_user(self) -> dict:
        return self.driver.users.get_user(user_id="me")

    @property
    # @cachedmethod(lambda self: self.cache["my_teams"], key=autotuple_hashkey)
    def my_teams(self) -> list:
        return self.driver.teams.get_user_teams(user_id=self.my_user["id"])

    @property
    def selected_team(self, teamnumber=0) -> dict:
        return self.my_teams[teamnumber]

    @property
    # @cachedmethod(lambda self: self.cache["known_users"], key=autotuple_hashkey)
    def known_users(self) -> list:
        return self.driver.users.get_users()

    def user_from_known_users(self, userid) -> dict:
        for user in self.known_users:
            if user["id"] == userid:
                return user

    def _convert_to_human_name(self, channel) -> str:
        if channel["type"] == "D":
            splitid = channel["name"].split("__")
            splitid.remove(self.my_user["id"])

            if splitid[0] in self.known_users:
                otheruser = self.user_from_known_users(splitid[0])

                if "nickname" in otheruser and otheruser["nickname"] != "":
                    return otheruser["nickname"]
                elif "first_name" in otheruser and otheruser["first_name"] != "":
                    if "last_name" in otheruser and otheruser["last_name"] != "":
                        return otheruser["first_name"] + " " + otheruser["last_name"]
                    else:
                        return otheruser["first_name"]
                else:
                    return otheruser["username"]

    @property
    @cachedasyncmethod(lambda self: self.cache["channels"], key=autotuple_hashkey)
    def channels(self) -> list:
        channellist = self.driver.channels.get_channels_for_user(
            user_id=self.my_user["id"], team_id=self.selected_team["id"]
        )
        for channel in channellist:
            if channel["display_name"] == "":
                channel["display_name"] = self._convert_to_human_name(channel)
        return channellist

    def cache_channel_posts(self, channel_id, params=None) -> list:
        return self.driver.posts.get_posts_for_channel(channel_id, params)

    def cache_all_channel_posts(self) -> None:
        for channel in self.channel_list:
            print("Cacheing channel: " + channel["name"])
            self.cache_channel_posts(channel["id"])

    @property
    # @cachedasyncmethod(lambda self: self.cache["posts"], key=autotuple_hashkey)
    def posts(self, channel_id, params=None) -> dict:
        channel_posts = self.driver.posts.get_posts_for_channel(channel_id, params)
        return channel_posts

    def get_posts_since_cache(self, channel_id) -> list:
        page = 0
        collided = False
        combinedposts = {"posts": {}}
        combinedorder = {"order": []}
        postinfo = {"next_post_id": None, "prev_post_id": None}
        while not collided:
            oldposts = self.cache_channel_posts(channel_id)
            newposts = self.get_channel_posts(channel_id)

            for postid in newposts["posts"]:
                if postid in oldposts["posts"]:
                    collided = True
                else:
                    combinedposts["posts"][postid] = newposts["posts"][postid]
                    if newposts["next_post_id"] is not None:
                        postinfo["next_post_id"] = newposts["next_post_id"]
                    if newposts["prev_post_id"] is not None:
                        postinfo["prev_post_id"] = newposts["prev_post_id"]

            for order in newposts["order"]:
                if order not in oldposts["order"]:
                    combinedorder["order"].append(order)

            page += 1

        return combinedorder | combinedposts | postinfo

    def sort_posts_by_date(self, posts) -> list:
        return sorted(posts, key=lambda x: x["posts"]["create_at"])

    def sort_by_order(self, posts) -> list:
        order = sorted(posts, key=lambda x: x["order"])
        sortedposts = []
        for id in order:
            for post in posts["posts"]:
                if post["id"] == id:
                    sortedposts.append(post)

        return


if __name__ == "__main__":
    import configstore
    import pprint

    pp = pprint.PrettyPrinter(indent=4)

    config = configstore.load_config("/home/mark/.config/matterless/mmless.ini")

    mmm = MattermostManager(
        options={
            "url": config["matterless"]["url"],
            "token": config["matterless"]["token"],
            "login_id": config["matterless"]["loginid"],
            "password": config["matterless"]["password"],
            "mfa_token": config["matterless"]["mfatoken"],
            "port": 443,
        }
    )

    # pp.pprint(mmm.get_posts_since_cache(channel_id="n4n9gwy6ej8fpkac8k6xwrdoyw"))
    # maxitems = 5
    # items = 0
    # for channel in mmm.channel_list:
    # print(channel)
    # pp.pprint(mmm.get_posts_since_cache(channel["id"]))
    # break

    # print(mmm.cache_channel_posts("n4n9gwy6ej8fpkac8k6xwrdoyw"))
    # print(mmm.driver.users.get_user("c5dzkyojjfnrtbogr37zqhshga"))
    pp.pprint(mmm.channels)
    # print(mmm.my_user)

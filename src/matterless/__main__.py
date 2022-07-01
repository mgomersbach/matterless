"""Command-line interface."""
import appdirs
import click
import configstore
import tui
import mattermost

USERAPPDIRS = appdirs.AppDirs("matterless", "Mark Gomersbach")


@click.command()
@click.version_option()
@click.option(
    "--configfile",
    "-c",
    default=USERAPPDIRS.user_config_dir + "/mmless.ini",
    help="Config file.",
)
@click.option("--url", "-u", help="Mattermost URL.")
@click.option("--token", "-t", help="Mattermost token.")
@click.option("--loginid", "-l", help="Mattermost login ID.")
@click.option("--password", "-p", help="Mattermost password.")
@click.option("--mfatoken", "-m", help="Mattermost MFA token.")
def main(configfile, url, token, loginid, password, mfatoken) -> None:
    """Matterless."""

    config = configstore.load_config(configfile)
    if "matterless" not in config:
        config["matterless"] = {}
    if url:
        config["matterless"]["url"] = url
    if token:
        config["matterless"]["token"] = token
    if loginid:
        config["matterless"]["loginid"] = loginid
    if password:
        config["matterless"]["password"] = password
    if mfatoken:
        config["matterless"]["mfatoken"] = mfatoken
    configstore.save_config(configfile, config)
    mmm = mattermost.MattermostManager(
        options={
            "url": config["matterless"]["url"],
            "token": config["matterless"]["token"],
            "login_id": config["matterless"]["loginid"],
            "password": config["matterless"]["password"],
            # "mfa_token": config["matterless"]["mfatoken"],
            "port": 443,
        }
    )
    with tui.Terminal(configfile=configfile, mattermost=mmm) as terminal:
        terminal.mainloop()


if __name__ == "__main__":
    main(prog_name="matterless")  # pragma: no cover

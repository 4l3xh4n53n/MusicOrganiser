class Album:
    """
    Represents a music album and stores any useful metadata and processing status
    """

    def __init__(self, title: str, date: int, downloading: bool, downloaded: bool, tags: bool, cover: bool,
                 replay_gain: bool, server_upload: bool, audio_format: str, markers: str, notes: str):
        """
        Initialises a new Album instance

        :param title: The title of the Album
        :param date: The release year of the Album
        :param downloading: True the album is in the process of downloading, False otherwise
        :param downloaded: True if the album download is complete, False otherwise
        :param tags: True if the albums tags have been sanitised and corrected, False otherwise
        :param cover: True if the album has a high-res cover, False otherwise
        :param replay_gain: True if ReplayGain has been calculated for the album, False otherwise
        :param server_upload: True if a copy has been re-encoded and uploaded to the streaming server, False otherwise
        :param audio_format: The audio format of the album, (e.g. "FLAC", "OGG")
        :param markers: Contains information to help keep track of albums
        :param notes: Any additional notes
        """
        self.title = title
        self.date = date
        self.downloading = downloading
        self.downloaded = downloaded
        self.tags = tags
        self.cover = cover
        self.replay_gain = replay_gain
        self.server_upload = server_upload
        self.format = audio_format
        self.markers = markers
        self.notes = notes


    @classmethod
    def from_dict(cls, data):
        """
        Creates an album instance from a dictionary.
        Useful for parsing data from MongoDB.

        :param data: Dictionary containing artist data
        :return: Album with data from the Dictionary
        """
        return cls(
            data.get("title"),
            data.get("date"),
            data.get("downloading"),
            data.get("downloaded"),
            data.get("tags"),
            data.get("cover"),
            data.get("replay_gain"),
            data.get("server_upload"),
            data.get("format"),
            data.get("markers"),
            data.get("notes")
        )


    def to_dict(self) -> dict:
        """
        Serialises the Album instance to a dictionary suitable for MongoDB

        :return: Dictionary of album instance
        """
        return {
            "title": self.title,
            "date": self.date,
            "downloading": self.downloading,
            "downloaded": self.downloaded,
            "tags": self.tags,
            "cover": self.cover,
            "replay_gain": self.replay_gain,
            "server_upload": self.server_upload,
            "format": self.format,
            "markers": self.markers,
            "notes": self.notes
        }


    def save(self, artist:str):
        """
        NOT IMPLEMENTED
        Saves changes to a single album in the database as opposed to re-writing the whole artist object.
        This is NOT IMPLEMENTED as I am unsure it's worth the extra code complexity and RAM usage
        """
        pass

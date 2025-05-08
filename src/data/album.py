class Album:
    def __init__(self, title: str, date: int, downloading: bool, downloaded: bool, tags: bool, cover: bool,
            replay_gain: bool, server_upload: bool, format: str, markers: str, notes: str):
        self.title = title
        self.date = date
        self.downloading = downloading
        self.downloaded = downloaded
        self.tags = tags
        self.cover = cover
        self.replay_gain = replay_gain
        self.server_upload = server_upload
        self.format = format
        self.markers = markers
        self.notes = notes


    @classmethod
    def from_dict(cls, data):
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


    def to_dict(self):
        return {
            "title": self.title,
            "date": self.date,
            # The option to set the album to downloading is given to save database calls and make things faster
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
        # todo, do I implement a single album save feature? Will it be useful? Will it be too complex?
        pass

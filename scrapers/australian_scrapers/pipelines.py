import csv
import os
from pathlib import Path


class CsvPipeline:
    """Save scraped items to timestamped CSV files in output/."""

    def open_spider(self, spider):
        self.files = {}

    def close_spider(self, spider):
        for f in self.files.values():
            f.close()

    def _ensure_writer(self, spider, item):
        name = spider.name
        if name not in self.files:
            out_dir = Path(spider.settings.get("FEED_URI", "output")).parent
            out_dir.mkdir(exist_ok=True)
            path = out_dir / f"{name}.csv"
            exists = path.exists()
            self.files[name] = {
                "file": open(path, "a" if exists else "w", newline="", encoding="utf-8"),
                "writer": None,
                "fields": list(item.keys()),
            }
        state = self.files[name]
        if state["writer"] is None:
            state["writer"] = csv.DictWriter(state["file"], fieldnames=state["fields"])
            if state["file"].mode == "w":
                state["writer"].writeheader()
        return state["writer"]

    def process_item(self, item, spider):
        writer = self._ensure_writer(spider, item)
        writer.writerow(dict(item))
        return item

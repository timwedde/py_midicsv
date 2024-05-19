### System ###
from pprint import pformat


class Pattern(list):
    useRunningStatus = True

    def __init__(self, tracks=None, resolution=220, format=1, tick_relative=True):
        self.format = format
        self.resolution = resolution
        self.tick_relative = tick_relative
        super().__init__(tracks or [])

    def __repr__(self):
        return f"midi.Pattern(format={self.format!r}, resolution={self.resolution!r}, tracks=\\\n{pformat(list(self))})"

    def make_ticks_abs(self):
        self.tick_relative = False
        for track in self:
            track.make_ticks_abs()

    def make_ticks_rel(self):
        self.tick_relative = True
        for track in self:
            track.make_ticks_rel()

    def __getitem__(self, item):
        if isinstance(item, slice):
            indices = item.indices(len(self))
            return Pattern(
                resolution=self.resolution,
                format=self.format,
                tracks=(super(Pattern, self).__getitem__(i) for i in range(*indices)),
            )
        else:
            return super().__getitem__(item)

    def __getslice__(self, i, j):
        # The deprecated __getslice__ is still called when subclassing
        # built-in types for calls of the form List[i:j]
        return self.__getitem__(slice(i, j))


class Track(list):
    def __init__(self, events=None, tick_relative=True):
        self.tick_relative = tick_relative
        super().__init__(events or [])

    def make_ticks_abs(self):
        if self.tick_relative:
            self.tick_relative = False
            running_tick = 0
            for event in self:
                event.tick += running_tick
                running_tick = event.tick

    def make_ticks_rel(self):
        if not self.tick_relative:
            self.tick_relative = True
            running_tick = 0
            for event in self:
                event.tick -= running_tick
                running_tick += event.tick

    def __getitem__(self, item):
        if isinstance(item, slice):
            indices = item.indices(len(self))
            return Track(super(Track, self).__getitem__(i) for i in range(*indices))
        else:
            return super().__getitem__(item)

    def __getslice__(self, i, j):
        # The deprecated __getslice__ is still called when subclassing
        # built-in types for calls of the form List[i:j]
        return self.__getitem__(slice(i, j))

    def __repr__(self):
        return "Track(\\\n  {})".format(pformat(list(self)).replace("\n", "\n  "))

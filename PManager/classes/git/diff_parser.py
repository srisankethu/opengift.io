        if not raw.startswith("commit"):
            raise IOError("Cannot parse unparsable diff")
        if self.raw[start + 3].startswith("Binary files"):
            pattern = re.compile('Binary files "?a?(?P<old_path>[A-zА-я0-9_\/. -]+)"?' +
                                 ' and "?b?(?P<new_path>[A-zА-я0-9_\/. -]+)"? differ')
            m = pattern.search(self.raw[start + 3])
            if m:
                mode = False
                (old_path, new_path) = m.groups()
                if old_path == '/dev/null':
                    mode = "C"
                    file_obj['path'] = new_path
                elif new_path == '/dev/null':
                    mode = "D"
                    file_obj['path'] = old_path
                else:
                    file_obj['path'] = new_path
                file_obj['action'] = mode
                file_obj['diff'] = False
                file_obj['lines'] = []
                file_obj['summary'] = {
                    "deleted": 1 if mode == "D" else 0,
                    "created": 1 if mode == "C" else 0,
                    "binary": True
                }
                return file_obj
            "created": self.__get_line_count('created', file_obj['lines']),
            "binary": False
        (ln, lo) = (0, 0)
            if diff_line.startswith("\ No newline"):
                continue
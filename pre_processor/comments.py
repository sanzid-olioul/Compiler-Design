class DeleteComments:
    def __init__(self,raw_source_code):
        self.raw_source_code = raw_source_code
        self._comment_indexes = []
        self.source_code = None

    def __call__(self):
        self._find_comments('//', '\n') # For finding single line comments
        self._find_comments('/*', '*/') # For finding multiple line comments
        self.source_code = self._delete_comments()
        return self.source_code

    def _find_comments(self,begin_str,end_str):
        current_index = self.raw_source_code.find(begin_str, 0)
        while current_index != -1:
            next_end_index = self.raw_source_code.find(end_str, current_index)
            if next_end_index == -1:
                self._comment_indexes.append((current_index, len(self.raw_source_code) - 1))
            else:
                self._comment_indexes.append((current_index, next_end_index + len(end_str) - 1))
            current_index = self.raw_source_code.find('//', next_end_index)

    def _delete_comments(self):
        if len(self._comment_indexes) == 0:
            return self.raw_source_code
        new_code = []
        curr_index = 0
        for i, (start, end) in enumerate(self._comment_indexes):
            new_code.append(self.raw_source_code[curr_index:start])
            curr_index = end + 1
            if i == len(self._comment_indexes) - 1:
                new_code.append(self.raw_source_code[curr_index:len(self.raw_source_code)])
        return ''.join(new_code)
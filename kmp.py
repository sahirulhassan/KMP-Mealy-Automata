def compute_lps(pattern: str) -> list[int]:
    """
    Compute the LPS (Longest Proper Prefix which is also Suffix) array.

    lps[i] = length of the longest proper prefix of pattern[0..i]
             which is also a suffix ending at index i.
    """
    pattern_length = len(pattern)
    lps = [0] * pattern_length

    prefix_length = 0      # length of current longest prefix-suffix
    current_index = 1      # start from second character

    while current_index < pattern_length:
        if pattern[current_index] == pattern[prefix_length]:
            prefix_length += 1
            lps[current_index] = prefix_length
            current_index += 1
        else:
            if prefix_length != 0:
                prefix_length = lps[prefix_length - 1]
            else: # prefix_length == 0
                lps[current_index] = 0
                current_index += 1

    print("LPS Array: ", lps)
    return lps


class KMPString:
    """
    Implements KMP-based string searching on a fixed text.

    Supported operations:
    - contains(pattern)
    - count(pattern): non-overlapping occurrences
    - startsWith(pattern)
    - endsWith(pattern)

    Alphabet restricted to {'a', 'b'} or {'0', '1'}.
    """

    def __init__(self, text: str):
        allowed_characters = {'a', 'b', '0', '1'}
        if not set(text).issubset(allowed_characters):
            raise ValueError(
                f"Text contains illegal characters. Allowed: {allowed_characters}"
            )

        self.text = text

    def contains(self, pattern: str) -> bool:
        if pattern == "":
            return True

        lps = compute_lps(pattern)

        text_index = 0
        pattern_index = 0

        while text_index < len(self.text):
            if self.text[text_index] == pattern[pattern_index]:
                text_index += 1
                pattern_index += 1

                if pattern_index == len(pattern):
                    return True
            else:
                if pattern_index != 0:
                    pattern_index = lps[pattern_index - 1]
                else: # pattern_index == 0
                    text_index += 1

        return False

    def count(self, pattern: str) -> int:
        """
        Count non-overlapping occurrences of pattern in the text.
        """
        if pattern == "":
            return len(self.text) + 1

        lps = compute_lps(pattern)

        text_index = 0
        pattern_index = 0
        occurrence_count = 0

        text_length = len(self.text)
        pattern_length = len(pattern)

        while text_index < text_length:
            if self.text[text_index] == pattern[pattern_index]:
                text_index += 1
                pattern_index += 1

                if pattern_index == pattern_length:
                    occurrence_count += 1
                    pattern_index = 0  # reset for non-overlapping match
            else:
                if pattern_index != 0:
                    pattern_index = lps[pattern_index - 1]
                else:
                    text_index += 1

        return occurrence_count

    def startsWith(self, pattern: str) -> bool:
        return self.text.startswith(pattern)

    def endsWith(self, pattern: str) -> bool:
        return self.text.endswith(pattern)

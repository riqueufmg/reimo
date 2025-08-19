/**
 * Returns the number of characters between the current position and the next instance of the input sequence
 *
 * @param seq scan target
 * @return offset between current position and next instance of target. -1 if not found.
 */
int nextIndexOf(CharSequence seq) {
    bufferUp();
    // doesn't handle scanning for surrogates
    char startChar = seq.charAt(0);
    for (int offset = bufPos; offset < bufLength; offset++) {
        // scan to first instance of startchar:
        if (startChar != charBuf[offset])
            while (++offset < bufLength && startChar != charBuf[offset]) {
                /* empty */
            }
        int i = offset + 1;
        int last = i + seq.length() - 1;
        if (offset < bufLength && last <= bufLength) {
            for (int j = 1; i < last && seq.charAt(j) == charBuf[i]; i++, j++) {
                /* empty */
            }
            if (// found full sequence
            i == last)
                return offset - bufPos;
        }
    }
    return -1;
}

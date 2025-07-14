/**
 * Encode the given symbol info to a bit matrix.
 *
 * @param placement  The DataMatrix placement.
 * @param symbolInfo The symbol info to encode.
 * @return The bit matrix generated.
 */
private static BitMatrix encodeLowLevel(DefaultPlacement placement, SymbolInfo symbolInfo, int width, int height) {
    int symbolWidth = symbolInfo.getSymbolDataWidth();
    int symbolHeight = symbolInfo.getSymbolDataHeight();
    ByteMatrix matrix = new ByteMatrix(symbolInfo.getSymbolWidth(), symbolInfo.getSymbolHeight());
    int matrixY = 0;
    for (int y = 0; y < symbolHeight; y++) {
        // Fill the top edge with alternate 0 / 1
        int matrixX;
        if ((y % symbolInfo.matrixHeight) == 0) {
            matrixX = 0;
            for (int x = 0; x < symbolInfo.getSymbolWidth(); x++) {
                matrix.set(matrixX, matrixY, (x % 2) == 0);
                matrixX++;
            }
            matrixY++;
        }
        matrixX = 0;
        for (int x = 0; x < symbolWidth; x++) {
            // Fill the right edge with full 1
            if ((x % symbolInfo.matrixWidth) == 0) {
                matrix.set(matrixX, matrixY, true);
                matrixX++;
            }
            matrix.set(matrixX, matrixY, placement.getBit(x, y));
            matrixX++;
            // Fill the right edge with alternate 0 / 1
            if ((x % symbolInfo.matrixWidth) == symbolInfo.matrixWidth - 1) {
                matrix.set(matrixX, matrixY, (y % 2) == 0);
                matrixX++;
            }
        }
        matrixY++;
        // Fill the bottom edge with full 1
        if ((y % symbolInfo.matrixHeight) == symbolInfo.matrixHeight - 1) {
            matrixX = 0;
            for (int x = 0; x < symbolInfo.getSymbolWidth(); x++) {
                matrix.set(matrixX, matrixY, true);
                matrixX++;
            }
            matrixY++;
        }
    }
    return convertByteMatrixToBitMatrix(matrix, width, height);
}

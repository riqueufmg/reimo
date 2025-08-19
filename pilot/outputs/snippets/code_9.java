public void handleLine(final String inLine) {
    // JMH ???
    String line = inLine.replaceFirst("^ +", "");
    line = StringUtil.replaceXMLEntities(line);
    String trimmedLine = line.trim();
    if (DEBUG_LOGGING_ASSEMBLY) {
        logger.debug("handleLine:{}", line);
    }
    if (line.startsWith("[Disassembling for mach")) {
        architecture = Architecture.parseFromLogLine(line);
        if (architecture == null) {
            logger.error("Could not determine architecture from '{}'", line);
        } else {
            if (DEBUG_LOGGING_ASSEMBLY) {
                logger.debug("Detected architecture: {}", architecture);
            }
        }
    }
    if (S_HASH.equals(previousLine) && line.startsWith("{method}")) {
        if (DEBUG_LOGGING_ASSEMBLY) {
            logger.debug("fixup mangled {method} line");
        }
        line = S_HASH + S_SPACE + line;
    }
    if (trimmedLine.startsWith("total in heap")) {
        String possibleNativeAddress = getStartAddress(line);
        if (possibleNativeAddress != null) {
            nativeAddress = possibleNativeAddress.trim();
        }
    }
    if (trimmedLine.endsWith(" bytes") || trimmedLine.startsWith("main code")) {
        String possibleEntryAddress = getStartAddress(line);
        if (possibleEntryAddress != null) {
            entryAddress = possibleEntryAddress.trim();
        }
    }
    if (trimmedLine.endsWith("</print_nmethod>")) {
        complete();
    }
    if (line.startsWith(NATIVE_CODE_START) || line.startsWith("Compiled method") || line.startsWith("----------------------------------------------------------------------")) {
        if (DEBUG_LOGGING_ASSEMBLY) {
            logger.debug("Assembly started");
        }
        assemblyStarted = true;
        if (builder.length() > 0) {
            complete();
        }
        String possibleNativeAddress = StringUtil.getSubstringBetween(line, NATIVE_CODE_START, S_COLON);
        if (possibleNativeAddress != null) {
            nativeAddress = possibleNativeAddress.trim();
        }
    } else if (assemblyStarted) {
        boolean couldBeNativeMethodMark = false;
        couldBeNativeMethodMark = line.startsWith(NATIVE_CODE_METHOD_MARK);
        if (couldBeNativeMethodMark) {
            if (DEBUG_LOGGING_ASSEMBLY) {
                logger.debug("Assembly method started");
            }
            methodStarted = true;
            if (!line.endsWith(S_APOSTROPHE)) {
                if (DEBUG_LOGGING_ASSEMBLY) {
                    logger.debug("Method signature interrupted");
                }
                methodInterrupted = true;
            }
        } else if (methodInterrupted && line.endsWith(S_APOSTROPHE)) {
            methodInterrupted = false;
        }
        if (methodStarted && line.length() > 0) {
            builder.append(line);
            if (!methodInterrupted) {
                builder.append(S_NEWLINE);
            }
        }
    }
    previousLine = line;
}

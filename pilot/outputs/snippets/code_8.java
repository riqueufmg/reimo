private void visitTagEliminateLock(Tag tagEliminateLock, IParseDictionary parseDictionary) {
    String kind = tagEliminateLock.getAttributes().get(ATTR_KIND);
    List<Tag> childrenJVMS = tagEliminateLock.getNamedChildren(TAG_JVMS);
    if (childrenJVMS.size() > 0) {
        for (Tag tagJVMS : childrenJVMS) {
            Map<String, String> tagJVMSAttributes = tagJVMS.getAttributes();
            String attrBCI = tagJVMSAttributes.get(ATTR_BCI);
            int bciValue = 0;
            if (attrBCI != null) {
                try {
                    bciValue = Integer.parseInt(attrBCI);
                } catch (NumberFormatException nfe) {
                    logger.error("Couldn't parse bci attribute {} tag {}", attrBCI, tagJVMS.toString(true));
                    continue;
                }
            } else {
                logger.error("Missing bci attribute on tag {}", tagJVMS.toString(true));
            }
            String methodID = tagJVMSAttributes.get(ATTR_METHOD);
            BCIOpcodeMap bciOpcodeMap = parseDictionary.getBCIOpcodeMap(methodID);
            //logger.info("current {} methodID {} parseMethod {}", currentMember.toStringUnqualifiedMethodName(true, true), methodID, parseDictionary.getParseMethod());
            if (CompilationUtil.memberMatchesMethodID(currentMember, methodID, parseDictionary)) {
                storeElidedLock(currentMember, bciValue, kind, bciOpcodeMap);
            } else if (processAnnotationsForInlinedMethods) {
                IMetaMember inlinedMember = findMemberForInlinedMethod(tagJVMS, parseDictionary);
                if (inlinedMember != null) {
                    storeElidedLock(inlinedMember, bciValue, kind, bciOpcodeMap);
                } else {
                    unhandledTags.add(tagJVMS);
                }
            }
        }
        // end for
    }
}

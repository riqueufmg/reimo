private Object processSingle(Page page, String html, boolean isRaw) {
    Object o = null;
    try {
        o = clazz.newInstance();
        for (FieldExtractor fieldExtractor : fieldExtractors) {
            if (fieldExtractor.isMulti()) {
                List<String> value;
                switch(fieldExtractor.getSource()) {
                    case RawHtml:
                        value = page.getHtml().selectDocumentForList(fieldExtractor.getSelector());
                        break;
                    case Html:
                        if (isRaw) {
                            value = page.getHtml().selectDocumentForList(fieldExtractor.getSelector());
                        } else {
                            value = fieldExtractor.getSelector().selectList(html);
                        }
                        break;
                    case Url:
                        value = fieldExtractor.getSelector().selectList(page.getUrl().toString());
                        break;
                    case RawText:
                        value = fieldExtractor.getSelector().selectList(page.getRawText());
                        break;
                    default:
                        value = fieldExtractor.getSelector().selectList(html);
                }
                if ((value == null || value.size() == 0) && fieldExtractor.isNotNull()) {
                    return null;
                }
                if (fieldExtractor.getObjectFormatter() != null) {
                    List<Object> converted = convert(value, fieldExtractor.getObjectFormatter());
                    setField(o, fieldExtractor, converted);
                } else {
                    setField(o, fieldExtractor, value);
                }
            } else {
                String value;
                switch(fieldExtractor.getSource()) {
                    case RawHtml:
                        value = page.getHtml().selectDocument(fieldExtractor.getSelector());
                        break;
                    case Html:
                        if (isRaw) {
                            value = page.getHtml().selectDocument(fieldExtractor.getSelector());
                        } else {
                            value = fieldExtractor.getSelector().select(html);
                        }
                        break;
                    case Url:
                        value = fieldExtractor.getSelector().select(page.getUrl().toString());
                        break;
                    case RawText:
                        value = fieldExtractor.getSelector().select(page.getRawText());
                        break;
                    default:
                        value = fieldExtractor.getSelector().select(html);
                }
                if (value == null && fieldExtractor.isNotNull()) {
                    return null;
                }
                if (fieldExtractor.getObjectFormatter() != null) {
                    Object converted = convert(value, fieldExtractor.getObjectFormatter());
                    if (converted == null && fieldExtractor.isNotNull()) {
                        return null;
                    }
                    setField(o, fieldExtractor, converted);
                } else {
                    setField(o, fieldExtractor, value);
                }
            }
        }
        if (AfterExtractor.class.isAssignableFrom(clazz)) {
            ((AfterExtractor) o).afterProcess(page);
        }
    } catch (InstantiationException e) {
        logger.error("extract fail", e);
    } catch (IllegalAccessException e) {
        logger.error("extract fail", e);
    } catch (InvocationTargetException e) {
        logger.error("extract fail", e);
    }
    return o;
}

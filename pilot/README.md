### Pre-requisites:
1. Python 3.9
2. HugginFace API token
3. Valid and Active HugginFace Endpoint API

### Pilot Execution:
1. On repository root, execute:
    > python .\scripts\main.py

### The script will:
1. Extract methods in .data/repositories/ referenced in .data/samples.csv

### Method Toolkit Examples:
java -jar tools/method-toolkit-1.0.jar extract data/repositories/jsoup-master/src/main/java/org/jsoup/nodes/Node.java 439

java -jar tools/method-toolkit-1.0.jar backup data/repositories/jsoup-master/src/main/java/org/jsoup/nodes/Node.java

java -jar tools/method-toolkit-1.0.jar replace data/repositories/jsoup-master/src/main/java/org/jsoup/nodes/Node.java 439 outputs/codellama7binstruct/refactorings/refactored_code_34.java

java -jar tools/method-toolkit-1.0.jar restore data/repositories/jsoup-master/src/main/java/org/jsoup/nodes/Node.java
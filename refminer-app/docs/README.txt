false:
mvn exec:java -Dexec.mainClass="com.example.refminer.App" -Dexec.args="--mode=identify --start=36287f7c3b09eff78395267a3ac0d7da067863fd --end=40950c317bd52ea5ce4cf0d19707fe426b66649c --repo=https://github.com/danilofes/refactoring-toy-example.git --type=RENAME_METHOD" -Dorg.slf4j.simpleLogger.log.org.refactoringminer=error

true:
mvn exec:java -Dexec.mainClass="com.example.refminer.App" -Dexec.args="--mode=identify --start=36287f7c3b09eff78395267a3ac0d7da067863fd --end=40950c317bd52ea5ce4cf0d19707fe426b66649c --repo=https://github.com/danilofes/refactoring-toy-example.git --type=EXTRACT_OPERATION" -Dorg.slf4j.simpleLogger.log.org.refactoringminer=error

mvn exec:java -Dexec.mainClass="com.example.refminer.App" -Dexec.args="--mode=list --start=36287f7c3b09eff78395267a3ac0d7da067863fd --end=40950c317bd52ea5ce4cf0d19707fe426b66649c --repo=https://github.com/danilofes/refactoring-toy-example.git" -Dorg.slf4j.simpleLogger.log.org.refactoringminer=error


Alluxio:
mvn exec:java -Dexec.mainClass="com.example.refminer.App" -Dexec.args="--mode=identify --start=9d2ab8ed202cf7a4e05746e35b29383ff24fff93 --end=3f21b2d3aceb778fd92fc511a853355cee2f3734 --repo=https://github.com/Alluxio/alluxio.git --type=EXTRACT_OPERATION" -Dorg.slf4j.simpleLogger.log.org.refactoringminer=error

mvn exec:java -Dexec.mainClass="com.example.refminer.App" -Dexec.args="--mode=list --start=9d2ab8ed202cf7a4e05746e35b29383ff24fff93 --end=3f21b2d3aceb778fd92fc511a853355cee2f3734 --repo=https://github.com/Alluxio/alluxio.git" -Dorg.slf4j.simpleLogger.log.org.refactoringminer=error

Jsoup:
mvn exec:java -Dexec.mainClass="com.example.refminer.App" -Dexec.args="--mode=identify --start=7693192fb34380328936a73f8c8cc346893a457a --end=2b3c4e17d9b42a54957463cebc763213da7ea00d --repo=https://github.com/jhy/jsoup.git --type=EXTRACT_OPERATION" -Dorg.slf4j.simpleLogger.log.org.refactoringminer=error

mvn exec:java -Dexec.mainClass="com.example.refminer.App" -Dexec.args="--mode=list --start=7693192fb34380328936a73f8c8cc346893a457a --end=2b3c4e17d9b42a54957463cebc763213da7ea00d --repo=https://github.com/jhy/jsoup.git" -Dorg.slf4j.simpleLogger.log.org.refactoringminer=error
package com.example.refminer;

import org.eclipse.jgit.lib.Repository;
import org.refactoringminer.api.*;
import org.refactoringminer.rm1.GitHistoryRefactoringMinerImpl;
import org.refactoringminer.util.GitServiceImpl;

import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class App {

    private final String startCommit;
    private final String endCommit;
    private final String repoUrl;
    private final Repository repo;
    private final RefactoringType refactoringType;
    private final String mode;
    private int c = 0;

    public App(Map<String, String> argsMap) throws Exception {
        if (!argsMap.containsKey("start")) throw new IllegalArgumentException("Missing argument: --start");
        if (!argsMap.containsKey("end")) throw new IllegalArgumentException("Missing argument: --end");
        if (!argsMap.containsKey("repo")) throw new IllegalArgumentException("Missing argument: --repo");
        if (!argsMap.containsKey("mode")) throw new IllegalArgumentException("Missing argument: --mode");

        this.startCommit = argsMap.get("start");
        this.endCommit = argsMap.get("end");
        this.repoUrl = argsMap.get("repo");
        this.mode = argsMap.get("mode");

        if (argsMap.containsKey("type")) {
            this.refactoringType = RefactoringType.valueOf(argsMap.get("type"));
        } else {
            this.refactoringType = null;
        }

        GitService gitService = new GitServiceImpl();

        String repoName = repoUrl.substring(repoUrl.lastIndexOf('/') + 1).replace(".git", "");
        String localPath = "tmp/" + repoName;

        this.repo = gitService.cloneIfNotExists(localPath, repoUrl);

        // Faz fetch usando JGit diretamente para garantir que os commits estejam disponíveis
        try (Git git = new Git(repo)) {
            git.fetch().call();
        } catch (GitAPIException e) {
            throw new RuntimeException("Failed to fetch from remote repository", e);
        }
    }

    public void identifyRefactoringInstances() throws Exception {
        if (refactoringType == null) {
            throw new IllegalArgumentException("Missing argument: --type (required for mode identify)");
        }

        GitHistoryRefactoringMiner miner = new GitHistoryRefactoringMinerImpl();

        miner.detectBetweenCommits(repo, startCommit, endCommit, new RefactoringHandler() {
            @Override
            public void handle(String commitId, List<Refactoring> refactorings) {
                for (Refactoring ref : refactorings) {
                    if (ref.getRefactoringType() == refactoringType) {
                        c++;
                    }
                }
            }
        });

        System.out.println("[refactoring_itentification]" + (c > 0) + "[\\refactoring_itentification]");
    }

    public void listRefactoringInstances() throws Exception {
        GitHistoryRefactoringMiner miner = new GitHistoryRefactoringMinerImpl();

        miner.detectBetweenCommits(repo, startCommit, endCommit, new RefactoringHandler() {
            @Override
            public void handle(String commitId, List<Refactoring> refactorings) {                
                for (Refactoring ref : refactorings) {
                    System.out.println(ref.getRefactoringType());
                }
            }
        });
    }

    public static void main(String[] args) throws Exception {
        Map<String, String> argsMap = new HashMap<>();
        for (String arg : args) {
            if (arg.startsWith("--") && arg.contains("=")) {
                String[] parts = arg.substring(2).split("=", 2);
                argsMap.put(parts[0], parts[1]);
            }
        }

        try {
            App app = new App(argsMap);

            switch (argsMap.get("mode")) {
                case "identify":
                    app.identifyRefactoringInstances();
                    break;
                case "list":
                    System.out.println("[refactoring_list]");
                    app.listRefactoringInstances();
                    System.out.println("[\\refactoring_list]");
                    break;
                default:
                    System.out.println("Invalid --mode. Use 'identify' or 'list'.");
            }
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }

        System.exit(0);
    }
}
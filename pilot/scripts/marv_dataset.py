import json
import pandas as pd

def get_validated_refactorings(refactoring_type, MaRV_path):
    refactorings = []

    with open(MaRV_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    extract_method_data = data.get(refactoring_type, [])

    df = pd.DataFrame(extract_method_data)

    for index, row in df.iterrows():
        sum = 0
        for vote in row.evaluations:
            sum += vote["vote"]
        
        if sum == 2:
            refactoring = {
                "refactoring_id": row.refactoring_id,
                "commit_sha": row.commit_sha,
                "commit_link": row.commit_link,
                "file_path": row.file_path,
                "description": row.description,
                "code_before": row.code_before,
                "code_after": row.code_after
            }
            refactorings.append(refactoring)

    return refactorings

extract_method_list = get_validated_refactorings("Extract Method", "data/MaRV.json")
rename_method_list = get_validated_refactorings("Rename Method", "data/MaRV.json")
rename_variable_list = get_validated_refactorings("Rename Variable", "data/MaRV.json")
remove_parameter_list = get_validated_refactorings("Remove Parameter", "data/MaRV.json")

print(len(extract_method_list), "Extract Method refactorings")
print(len(rename_method_list), "Rename Method refactorings")
print(len(rename_variable_list), "Rename Variable refactorings")
print(len(remove_parameter_list), "Remove Parameter refactorings")

# Example of how to access the first refactoring's code before
#print(extract_method_list[0]["code_before"])
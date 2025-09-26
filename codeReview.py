import requests
import validators
import json
import urllib.parse
import ollama

code_review_url = input("Enter the url of the code review: ")

generated_comments = {}

if validators.url(code_review_url):
    code_review_list = code_review_url.split("/")
    base_url = code_review_list[0] + "//" + code_review_list[2] + "/changes/"
    change_id = code_review_list[-2] if code_review_list[-1] == "" else code_review_list[-1]

    # Get current revision number for patch
    revisions_response_json = requests.get(base_url + change_id + "?o=ALL_REVISIONS")
    if revisions_response_json.status_code == 200:
        revisions_response = json.loads(revisions_response_json.content[4:])
        revision_id = revisions_response["current_revision"]

        # Get all changed files
        file_ids_response_json = requests.get(base_url + change_id + "/revisions/" + revision_id + "/files")
        if file_ids_response_json.status_code == 200:
            file_ids_response = json.loads(file_ids_response_json.content[4:])
            file_ids = list(file_ids_response.keys())

            # Get reviewer comments
            reviewer_comments_response_json = requests.get(base_url + change_id + "/revisions/" + revision_id + "/comments/")
            if reviewer_comments_response_json.status_code == 200:
                reviewer_comments = json.loads(reviewer_comments_response_json.content[4:])
            else:
                print("No reviewer comments found or URL failed to get success response")
            
            prompt_file = open("prompt.txt")
            prompt = prompt_file.read()
            prompt_file.close()

            n = len(file_ids)
            i = 1

            for file_id in file_ids:
                print(f"[{i}/{n}] Processing file: {file_id}")
                encoded_file_id = urllib.parse.quote_plus(file_id)
                
                # Get difference in file
                diff_response_json = requests.get(base_url + change_id + "/revisions/" + revision_id + "/files/" + encoded_file_id + "/diff?intraline")
                if diff_response_json.status_code == 200:
                    diff_response = diff_response_json.text[4:]

                    if file_id in reviewer_comments:
                        reviewed_lines = [x["line"] for x in reviewer_comments[file_id]]
                    else:
                        reviewed_lines = []

                    if len(diff_response) < 80000:  # GPT max input limit. Adjust if needed
                        gpt_response = ollama.chat(model="gemma3:4b",
                                            messages=[
                                                {"role": "user", "content": prompt.format(REVIEWED_LINES=reviewed_lines, FILE_DIFF=diff_response)}
                                            ])

                        generated_comments[file_id] = gpt_response['message']['content']
                    else:
                        print(f"[{i}/{n}] Skipping file: {file_id} as it exceeds input limit for model")
                else:
                    print(f"[{i}/{n}] Skipping file: {file_id} as unable to retrieve file diff")
                i += 1
        else:
            print("No changed files found for patch:", revision_id)
            input("Enter any key to quit...")
            quit()
    else:
        print("Patch is malformed or unable to retrieve patch information")
        input("Enter any key to quit...")
        quit()
    
    print("*********** Code Review Generation Complete ************")
    
    #Create markdown for comments
    markdown = f"# Code Review for Patch {change_id}\n\n"
    for file in generated_comments:
        markdown += f"## {file}\n{generated_comments[file]}\n"

    markdown_file = open("code_review_" + change_id + ".md", "w", encoding='utf-8')
    markdown_file.write(markdown)
    markdown_file.close()

    print("\nCode review generated in file:", "code_review_" + change_id + ".md")

else:
    print("URL provided is not valid\nRun program again with valid url")
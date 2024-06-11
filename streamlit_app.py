import pandas as pd
import requests
import json
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import time


def get_chromium_data(user):
    chromium_url = f"https://chromium-review.googlesource.com/changes/?q=author:{user}+status:merged"
    print("Invoking chromium-review web API...", chromium_url)
    response_chromium = requests.get(chromium_url)
    if response_chromium.status_code == 200:
        output_chromium = response_chromium.text
        output_json_chromium = json.loads(output_chromium[4:])
        if isinstance(output_json_chromium, list) and len(output_json_chromium) > 0:
            chromium_data = []
            for item in output_json_chromium:
                if isinstance(item, dict):
                    chromium_data.append({
                        "subject": item.get("subject", ""),
                        "project": item.get("project", ""),
                        "branch": item.get("branch", ""),
                        "status": item.get("status", ""),
                        "updated": item.get("updated", ""),
                        "User": user,
                        "Owner": user.split("@")[0],
                        "Repo": "Chromium",
                        "URL": chromium_url
                    })
                else:
                    print("Unexpected format of JSON data from chromium-review.")
            return chromium_data
    else:
        print(f"Failed to fetch data from chromium-review for user: {user}")

    return []

def get_android_data(user):
    android_url = f"https://android-review.googlesource.com/changes/?q=owner:{user}+status:merged"
    response_android = requests.get(android_url)
    if response_android.status_code == 200:
        output_android = response_android.text
        output_json_android = json.loads(output_android[4:])
        if isinstance(output_json_android, list) and len(output_json_android) > 0:
            android_data = []
            for item in output_json_android:
                if isinstance(item, dict):
                    android_data.append({
                        "subject": item.get("subject", ""),
                        "project": item.get("project", ""),
                        "branch": item.get("branch", ""),
                        "status": item.get("status", ""),
                        "updated": item.get("updated", ""),
                        "User": user,
                        "Owner": user.split("@")[0],
                        "Repo": "Android",
                        "URL": android_url
                    })
            return android_data
    return []


def get_gitlab_data(user):
    gitlab_url = f"https://gitlab.freedesktop.org/api/v4/projects/176/repository/commits?author={user}"
    response_gitlab = requests.get(gitlab_url)
    if response_gitlab.status_code == 200:
        output_gitlab = response_gitlab.text
        output_json_gitlab = json.loads(output_gitlab)
        if isinstance(output_json_gitlab, list) and len(output_json_gitlab) > 0:
            gitlab_data = []
            for item in output_json_gitlab:
                if isinstance(item, dict):
                    gitlab_data.append({
                        "subject": item.get("title", ""),
                        "project": "",
                        "branch": "",
                        "status": "",
                        "updated": item.get("committed_date", ""),
                        "User": user,
                        "Owner": user.split("@")[0],
                        "Repo": "GitLab",
                        "URL": gitlab_url
                    })
            return gitlab_data
    return []
def get_github_data(user_email, repo_name):
    if user_email:
        github_url = f"https://api.github.com/repos/{repo_name}/commits"
        params = {"author": user_email}
        try:
            response_github = requests.get(github_url, params=params)
            response_github.raise_for_status()
            output_github = response_github.json()
            if isinstance(output_github, list) and len(output_github) > 0:
                commits_data = []
                for commit in output_github:
                    if isinstance(commit, dict):
                        commits_data.append({
                            "subject": commit.get("commit", {}).get("message", ""),
                            "project": "",
                            "branch": "",
                            "status": "",
                            "updated": commit.get("commit", {}).get("committer", {}).get("date", ""),
                            "User": user_email,
                            "Owner": user_email.split("@")[0],
                            "Repo": "GitHub",
                            "URL": github_url
                        })
                commits_df = pd.DataFrame(commits_data)
                return commits_df
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data from GitHub: {e}")
    return pd.DataFrame()

# Streamlit application
st.title("Open Source Contribution Fetcher")

emails_input = st.text_input("Enter the email IDs of the persons (comma separated):")

# Checkboxes to select open-source repositories
chromium_selected = st.checkbox('Chromium')
android_selected = st.checkbox('Android')
gitlab_selected = st.checkbox('GitLab')
github_selected = st.checkbox('GitHub')

repo_name = []
if github_selected:
    repo_name = st.text_area("Enter GitHub repository names (comma separated):").split(',')

if st.button("Fetch Data"):
    if emails_input:
        email_list = [email.strip() for email in emails_input.split(",")]

        total_commits = 0
        no_commits_found = []
        all_data = []

        for email in email_list:
            chromium_data_df = pd.DataFrame()
            android_data_df = pd.DataFrame()
            gitlab_data_df = pd.DataFrame()
            github_data_df = pd.DataFrame()

            if chromium_selected:
                chromium_data_list = get_chromium_data(email)
                if chromium_data_list:
                    chromium_data_df = pd.DataFrame(chromium_data_list)
                else:
                    no_commits_found.append(f"Chromium: {email}")
                total_commits += len(chromium_data_df)

            if android_selected:
                android_data_list = get_android_data(email)
                if android_data_list:
                    android_data_df = pd.DataFrame(android_data_list)
                else:
                    no_commits_found.append(f"Android: {email}")
                total_commits += len(android_data_df)

            if gitlab_selected:
                gitlab_data_list = get_gitlab_data(email)
                if gitlab_data_list:
                    gitlab_data_df = pd.DataFrame(gitlab_data_list)
                else:
                    no_commits_found.append(f"GitLab: {email}")
                total_commits += len(gitlab_data_df)

            if github_selected and repo_name:
                github_data_list = [get_github_data(email, repo.strip()) for repo in repo_name]
                github_data_list = [data for data in github_data_list if not data.empty]
                if github_data_list:
                    github_data_df = pd.concat(github_data_list, ignore_index=True)
                else:
                    no_commits_found.append(f"GitHub: {email}")
                total_commits += len(github_data_df)

            # Consolidate all data for the current user
            user_data_df = pd.concat([chromium_data_df, android_data_df, gitlab_data_df, github_data_df],
                                     ignore_index=True)
            all_data.append(user_data_df)

        # Consolidate all data into a single DataFrame
        consolidated_df = pd.concat(all_data, ignore_index=True)

        # Display the consolidated data
        st.dataframe(consolidated_df)

        # Display the total number of commits
        st.subheader(f"Total Commits: {total_commits}")

        # Display the repositories with no commits found
        if no_commits_found:
            st.subheader("No commits found in the following repositories for the users:")
            st.write(", ".join(no_commits_found))

            # Extract the year from the "updated" column and count the number of commits per year
            consolidated_df['updated'] = pd.to_datetime(consolidated_df['updated'], errors='coerce')
            consolidated_df['year'] = consolidated_df['updated'].dt.year
            commits_per_year = consolidated_df['year'].value_counts().sort_index()

            # Plot the number of commits per year
            fig, ax = plt.subplots()
            commits_per_year.plot(kind='bar', ax=ax)
            ax.set_title("Number of Commits per Year")
            ax.set_xlabel("Year")
            ax.set_ylabel("Number of Commits")
            st.pyplot(fig)

            # Count the number of commits by open-source repository
            commits_by_repo = consolidated_df['Repo'].value_counts()

            # Plot the number of commits by open-source repository as a donut chart
            fig2, ax2 = plt.subplots()
            ax2.pie(commits_by_repo, labels=commits_by_repo.index, autopct='%1.1f%%', startangle=90,
                    wedgeprops={'width': 0.3})
            ax2.set_title("Number of Commits by Open Source Repository")
            st.pyplot(fig2)

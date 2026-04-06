from ai_agents.runtime.agent_runtime import AgentRuntime


def main():
    runtime = AgentRuntime()
    issue = runtime.get_jira_issue("SCRUM-1")

    print(issue)


if __name__ == "__main__":
    main()

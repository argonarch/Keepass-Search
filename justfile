project := "Keepass-Search"
task:
  task project:{{ project }} 
task-add *ARGS:
  task add project:{{ project }}  {{ ARGS }}

# [Scheduled Events and Task Queues](#scheduled-events-and-task-queues)

Two Mendix features for work that runs outside a user request. They are unrelated
and easy to confuse:

- A **scheduled event** is Mendix’s cron — it runs a microflow on a repeating
  schedule.
- A **task queue** bounds how many queued microflow calls run at once.

A scheduled event does **not** go through a task queue. Its own concurrency
control is `OnOverlap`, which decides what happens when a run is still going when
the next one is due.
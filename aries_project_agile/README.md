# Project Agile (Sprints & Reports)

This add-on extends Odoo's project management with agile methodologies, specifically focusing on Scrum-like sprint management and agile reporting.

## Features

- **Sprint Management**: Create and track sprints with states (Planned, Active, Closed).
- **Sprint Planning Board**: Specialized Kanban view to drag tasks between the Backlog and sprints.
- **Hour-Based Metrics**: Automatic tracking of Committed, Completed, Remaining, and Consumed hours (via timesheets) per sprint.
- **Lead & Cycle Time**: Automated calculation of task lead and cycle times (in days).
- **Agile Reports**:
  - **Sprint Velocity**: Compare completed vs. committed hours across sprints.
  - **Capacity vs Commitment**: Track team capacity against the workload.
  - **Cumulative Flow Diagram (CFD)**: Analyze task distribution by stage over time.
  - **Burndown & Burnup**: Monitor daily progress within a sprint.
- **Data Integrity**: Enforced rules like "one active sprint per project" and "consistent projects for tasks/sprints."

## Configuration

1. **Installation**:
   - Ensure you have `project`, `hr_timesheet`, and `portal` modules installed.
   - Install the `project_agile` module.
2. **Setup**:
   - No specific project-level toggle is required. Once installed, the agile menus and fields are available for all projects.
   - We recommend using the **Project > Sprints** menu to create your first sprint for a project.

## User Guide

### 1. Active Sprint Board
Go to **Project > Active Sprint**.
- This is your current work board.
- It shows only tasks for currently **Active** sprints.
- Tasks are grouped by **Stage** (To Do, In Progress, Done, etc.).
- Use this to track day-to-day progress.

### 2. Sprint Planning
Go to **Project > Sprint Planning**.
- This specialized board groups tasks by **Sprint**.
- Drag tasks from the **Backlog** (left column) to any **Planned** or **Active** sprint.
- Use the **Search Panel** on the left to filter the view by sprint.

### 3. Managing Sprints
Go to **Project > Sprints**.
- Use the **Kanban** view to see a summary of each sprint.
- Click the **Start** button on a card to activate a sprint.
- Click the **Close** button when the sprint is finished.
- One active sprint is allowed per project.

### 4. Task Management
In any task form, use the **Sprint** field (after Project) to assign a sprint.
- Automatic calculations for **Lead Time** and **Cycle Time** occur when tasks are closed.
- Assign **Allocated Hours** to track commitment.

### 5. Agile Reporting
Access professional agile charts via **Project > Reporting**:
- **Current Burndown**: Progress of all active sprints.
- **Sprint Velocity**: Comparison of Completed vs Committed hours over time.
- **Capacity vs Commitment**: Track team load.
- **Sprint CFD**: Cumulative Flow Diagram.
- Use the **Burndown/Burnup** smart buttons on the Sprint form for detailed per-sprint charts.

---
*Developed for Odoo 19 Community Edition.*

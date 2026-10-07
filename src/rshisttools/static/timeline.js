const statusLabels = {
  completed: "Completed",
  partial: "In progress",
  future: "Not started",
};

const timelineElement = document.querySelector("#timeline");
const focusElement = document.querySelector("#focus-content");
const countElement = document.querySelector("#update-count");
const visibleCountElement = document.querySelector("#visible-count");
const feedbackElement = document.querySelector("#feedback");
const filters = [...document.querySelectorAll(".filters input[data-status], .filters input[value]")];
const optionalToggle = document.querySelector("#show-optional");

let updates = [];
let focusedId = null;

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function visibleGoals(update) {
  return optionalToggle.checked
    ? update.goals
    : update.goals.filter((goal) => !goal.optional);
}

function makeGoalActions(update, goal) {
  const actions = element("div", "goal-actions");
  const completed = element("button", "goal-action", goal.completed ? "Completed" : "Complete");
  completed.type = "button";
  completed.disabled = goal.completed;
  completed.addEventListener("click", () => changeGoal("completed", update, goal));

  const backlog = element("button", "goal-action backlog-action", goal.backlogged ? "Backlogged" : "Backlog");
  backlog.type = "button";
  backlog.disabled = goal.completed || goal.backlogged;
  backlog.addEventListener("click", () => changeGoal("backlog", update, goal));
  actions.append(completed, backlog);
  return actions;
}

function makeGoalRow(update, goal, focused = false) {
  const row = element("div", focused ? "focus-goal" : "goal-row");
  if (goal.completed) row.classList.add("completed");

  if (!focused && goal.section) {
    row.append(element("p", "goal-category", goal.section));
  }
  const description = element("p", focused ? "focus-goal-text" : "goal-description", goal.text);
  if (goal.optional) description.append(element("span", "goal-badge", "Optional"));
  if (goal.backlogged) description.append(element("span", "goal-badge", "Backlogged"));
  row.append(description, makeGoalActions(update, goal));
  return row;
}

function makePopover(update) {
  const popover = element("div", "goal-popover");
  const goals = visibleGoals(update);
  popover.setAttribute("aria-label", `Goals for ${update.name}`);
  popover.append(element("p", "popover-title", `${goals.length} goals · ${update.name}`));
  if (goals.length === 0) {
    const message = optionalToggle.checked
      ? "No checklist goals are recorded for this update."
      : "No non-optional goals are recorded for this update.";
    popover.append(element("p", "empty-goals", message));
    return popover;
  }
  goals.forEach((goal) => popover.append(makeGoalRow(update, goal)));
  return popover;
}

function renderTimeline() {
  const visibleStatuses = new Set(filters.filter((filter) => filter.checked).map((filter) => filter.value));
  const visible = updates.filter((update) => visibleStatuses.has(update.status));
  timelineElement.replaceChildren();
  visibleCountElement.textContent = `${visible.length} SHOWN`;
  countElement.textContent = updates.length.toLocaleString();

  if (visible.length === 0) {
    timelineElement.append(element("p", "empty-goals", "No updates match the selected filters."));
    return;
  }

  let currentYear = "";
  let group;
  for (const update of visible) {
    const year = update.date.slice(0, 4);
    if (year !== currentYear) {
      currentYear = year;
      group = element("section", "year-group");
      group.setAttribute("aria-label", year);
      group.append(element("h3", "year-label", year));
      timelineElement.append(group);
    }

    const card = element("article", `update-card status-${update.status}`);
    if (update.id === focusedId) card.classList.add("is-focused");
    card.append(element("span", "timeline-marker"));

    const select = element("button", "update-select");
    select.type = "button";
    select.setAttribute("aria-label", `Focus ${update.name}, ${update.display_date}`);
    select.addEventListener("click", () => {
      focusedId = update.id;
      renderTimeline();
      renderFocus();
    });

    const main = element("span", "update-main");
    main.append(
      element("span", "update-name", update.name),
      element("span", "update-date", update.display_date),
    );
    select.append(main, element("span", "goal-count", `${visibleGoals(update).length} GOALS`));
    card.append(select, makePopover(update));
    group.append(card);
  }
}

function renderFocus() {
  const update = updates.find((item) => item.id === focusedId);
  if (!update) {
    focusElement.replaceChildren();
    const empty = element("div", "empty-focus");
    empty.append(
      element("span", "empty-icon", "↖"),
      element("p", "", "Select an update on the timeline to see its goals here."),
    );
    focusElement.append(empty);
    return;
  }

  focusElement.replaceChildren();
  const goals = visibleGoals(update);
  const status = element("p", `focus-status status-${update.status}`);
  status.append(element("span", "filter-dot"), document.createTextNode(statusLabels[update.status]));
  focusElement.append(
    status,
    element("h3", "focus-title", update.name),
    element("p", "focus-date", update.display_date),
  );

  const completedCount = goals.filter((goal) => goal.completed).length;
  const backlogCount = goals.filter((goal) => goal.backlogged).length;
  const summary = element("div", "focus-summary");
  for (const [value, label] of [
    [goals.length, "Goals shown"],
    [completedCount, "Completed"],
    [backlogCount, "Backlogged"],
    [goals.length - completedCount - backlogCount, "Remaining"],
  ]) {
    const cell = element("div", "summary-cell");
    cell.append(element("span", "summary-value", String(value)), element("span", "summary-label", label));
    summary.append(cell);
  }
  focusElement.append(summary);

  const heading = element("h4", "focus-goals-heading", "Current goals");
  heading.append(element("span", "", `${goals.length}`));
  focusElement.append(heading);
  if (goals.length === 0) {
    const message = optionalToggle.checked
      ? "No checklist goals are recorded for this update."
      : "No non-optional goals are recorded for this update.";
    focusElement.append(element("p", "empty-goals", message));
  } else {
    goals.forEach((goal) => focusElement.append(makeGoalRow(update, goal, true)));
  }
}

async function changeGoal(action, update, goal) {
  feedbackElement.classList.remove("is-error");
  feedbackElement.textContent = "";
  document.querySelectorAll(".goal-action").forEach((button) => { button.disabled = true; });

  try {
    const response = await fetch(`/api/goals/${action}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        update: update.id,
        update_name: update.name,
        line: goal.line,
        text: goal.text,
      }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.description || result.message || "Could not update the goal.");
    updates = result.updates;
    renderTimeline();
    renderFocus();
    feedbackElement.textContent = action === "completed" ? "Goal marked complete." : "Goal added to backlog.";
  } catch (error) {
    feedbackElement.classList.add("is-error");
    feedbackElement.textContent = error instanceof Error ? error.message : "Could not update the goal.";
    renderTimeline();
    renderFocus();
  }
}

filters.forEach((filter) => filter.addEventListener("change", renderTimeline));
optionalToggle.addEventListener("change", () => {
  renderTimeline();
  renderFocus();
});

fetch("/api/updates")
  .then(async (response) => {
    const result = await response.json();
    if (!response.ok) throw new Error(result.description || "Could not load updates.");
    updates = result.updates;
    const firstInProgress = updates.find((update) => update.status === "partial");
    const firstIncomplete = updates.find((update) => update.status === "future");
    focusedId = (firstInProgress || firstIncomplete || updates[0])?.id ?? null;
    renderTimeline();
    renderFocus();
  })
  .catch((error) => {
    timelineElement.replaceChildren(
      element("p", "error-state", `Unable to load the update archive: ${error.message}`),
    );
    feedbackElement.classList.add("is-error");
    feedbackElement.textContent = "Check that the web app can read the update folders.";
  });

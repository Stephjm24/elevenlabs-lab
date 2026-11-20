const projects = document.getElementById("projects");

function projectEntry(project) {
  const article = document.createElement("article");
  article.className = "project";

  function addText(tag, text, className) {
    const element = document.createElement(tag);
    element.textContent = text;
    if (className) element.className = className;
    article.append(element);
    return element;
  }

  if (project.pushes) addText("p", project.pushes, "label");
  addText("h3", project.title);
  if (project.hook) addText("p", project.hook);
  if (project.audio) {
    const audio = document.createElement("audio");
    audio.controls = true;
    audio.preload = "none";
    audio.src = project.audio;
    audio.setAttribute("aria-label", "Audio sample for " + project.title);
    article.append(audio);
  }
  if (project.caption) addText("p", project.caption);
  if (project.link) addText("a", "Open experiment").href = project.link;
  if (project.notes) addText("a", "Read the lab notes").href = project.notes;
  return article;
}

async function loadGallery() {
  try {
    const response = await fetch("projects.json");
    if (!response.ok) throw new Error("Gallery unavailable");
    const list = await response.json();
    if (!Array.isArray(list)) throw new Error("Invalid gallery index");

    if (list.length) {
      projects.replaceChildren(...list.map(projectEntry));
    } else {
      const empty = document.createElement("p");
      empty.className = "status";
      empty.textContent = "No experiments published yet.";
      projects.replaceChildren(empty);
    }
  } catch {
    // Preserve the working repository link from the HTML fallback.
    projects.querySelector(".status").prepend("The gallery couldn’t load. ");
  }
}

loadGallery();

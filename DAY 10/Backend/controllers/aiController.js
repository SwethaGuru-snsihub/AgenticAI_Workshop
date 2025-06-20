exports.generateJourney = (req, res) => {
    const profile = req.body;
  
    const profileSummary = {
      name: profile.name || "Unknown",
      role: profile.role,
      department: profile.department,
      location: profile.location || "Remote",
      experience: profile.experience || 0
    };
  
    const tasks = [
      { task: "Complete HR paperwork", day: 1, priority: "High" },
      { task: "Set up email & tools", day: 1, priority: "High" },
      { task: `Meet your ${profileSummary.department} team`, day: 2, priority: "Medium" },
      { task: `${profileSummary.role} onboarding training`, day: 2, priority: "High" }
    ];
  
    if (profileSummary.location === "Onsite") {
      tasks.push({ task: "Take office tour", day: 1, priority: "Low" });
    }
  
    res.status(200).json({
      profileSummary,
      onboardingJourney: tasks
    });
  };
  
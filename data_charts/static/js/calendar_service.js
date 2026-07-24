async function fetchCalendarData() {

    const url = `/data_charts/api/dashboard/calendar/`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching chart data:", error);
        return null;
    }
}


function updatePopover(day) {
    let trainingButton = document.getElementById("training-button");
    let nutritionButton = document.getElementById("nutrition-button");
    let weightingButton = document.getElementById("weighting-button");

    if (day.workout_type) {
        trainingButton.textContent = "View workout";
        trainingButton.href = day.viewWorkoutURL;
    } else {
        trainingButton.textContent = "Add workout";
        trainingButton.href = day.addWorkoutURL;
    }

    if (day.nutritionInfo) {
        nutritionButton.textContent = "View nutrition";
        nutritionButton.href = day.viewNutritionURL;
    } else {
        nutritionButton.textContent = "Add nutrition";
        nutritionButton.href = day.addNutritionURL;
    }

    if (day.weightInfo) {
        weightingButton.textContent = "View weight";
        weightingButton.href = day.viewWeightingURL;
    } else {
        weightingButton.textContent = "Add weighting";
        weightingButton.href = day.addWeightingURL;
    }
}


export { fetchCalendarData, updatePopover };
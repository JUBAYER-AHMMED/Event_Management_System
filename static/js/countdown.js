function startCountdown(targetIsoDate) {
    const targetDate = new Date(targetIsoDate);

    function pad(value) {
        return String(value).padStart(2, '0'); // ensures 2 digits
    }

    function update() {
        const now = new Date();
        let diff = targetDate - now;

        if (diff <= 0) {
            document.getElementById("days").innerText = "00";
            document.getElementById("hours").innerText = "00";
            document.getElementById("minutes").innerText = "00";
            document.getElementById("seconds").innerText = "00";
            return;
        }

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        diff %= 1000 * 60 * 60 * 24;

        const hours = Math.floor(diff / (1000 * 60 * 60));
        diff %= 1000 * 60 * 60;

        const minutes = Math.floor(diff / (1000 * 60));
        diff %= 1000 * 60;

        const seconds = Math.floor(diff / 1000);

        document.getElementById("days").innerText = `${pad(days)}`;
        document.getElementById("hours").innerText = `${pad(hours)}`;
        document.getElementById("minutes").innerText = `${pad(minutes)}`;
        document.getElementById("seconds").innerText = `${pad(seconds)}`;
    }

    update();
    setInterval(update, 1000);
}

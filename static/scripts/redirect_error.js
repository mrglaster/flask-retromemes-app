const delay = ms => new Promise(res => setTimeout(res, ms));
 
const redirect = async () => {
    await delay(5000);
    window.location.href = "feed";
};
redirect();
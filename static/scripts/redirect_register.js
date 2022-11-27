const delay = ms => new Promise(res => setTimeout(res, ms));
 
const redirect = async () => {
    await delay(2200);
    window.location.href = "register";
};
redirect();
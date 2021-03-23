const puppeteer= require('puppeteer');
const request = require('request-promise-native');
const poll = require('promise-poller').default;

const config = {
    sitekey: '6LfSswwUAAAAAHJf09SGVMposJGyUXWXqo_iZ-m4',
    pageurl: 'https://passportappointment.travel.state.gov/',
    apiKey: 'd54f6b1160e6e85be28e85d3bfc2e7c2'
}

const chromeOptions = {
    chromePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: false,
    slowMo: 80,
    defaultViewport: null
};

(async function main() {
    try{
    const browser = await puppeteer.launch(chromeOptions);

    const page = await browser.newPage();
    console.log(`Getting to ${config.pageurl}`);
    await page.goto(config.pageurl);

    const requestId = await initiateCaptchaRequest(config.apiKey);

    await page.waitForSelector('#rb-home-list-new');
    await page.click('#rb-home-list-new', {clickCount:1});
    await page.click('#btnHomeNext', {clickCount:1});
    await page.waitForSelector('#InternationalTravel-yes');
    await page.click('#InternationalTravel-yes', {clickCount:1});
    await page.waitForSelector('#DateTravel');
    await page.type('#DateTravel', "04/07/2021");
    await page.click('#VisaNeeded-no',{clickCount:1});
    await page.$eval('button[data-val="2"]', el => el.click());

    const response = await pollForRequestResults(config.apiKey, requestId);

    console.log(`Entering recaptcha response ${response}`);

    await page.evaluate(`document.getElementById("g-recaptcha-response").innerHTML="${response}";`);

    console.log(`Submitting...`)

    await page.$eval('input[type=submit]', el => el.click());

    // Select agancy page afther pass recaptcha
    await page.waitForSelector('#SearchCriteria');
    await page.type('#SearchCriteria', "00921");
    await page.$eval(`button[class="btn-standard btn submitLocation"]`, el => el.click());
    await page.waitForSelector('button[class="btn-standard agency-select"]');
    await page.$eval('button[class="btn-standard agency-select"]', el => el.click());

    // Select an Appointment at: page
    console.log(`Navigating Select an Appointment at:... page`);
    await page.waitForSelector('a[class="flex-next"]');
    await page.$eval('a[class="flex-next"]', el => el.click());
    await page.waitForSelector('h3[class="bg-icon"]');
    await page.$eval('h3[class="bg-icon"]', el => el.click());
    await page.waitForSelector('div[class="slots"]');
    await page.click('.slots > span:nth-child(1)');
    await page.$eval('input[type="submit"]', el => el.click());

    //You now have a tentative reservation page
    console.log(`Navigating You now have a tentative reservation page`);
    await page.waitForSelector('div[class="editor-field"]');
    await page.type('#EmailAddress', "jemn1jemn@gmail.com");
    await page.waitForSelector('#PhoneNumber');
    await page.type('PhoneNumber', "7876739476");
    await page.type('#PIN', "1234");
    await page.type('#PINConfirm', "1234");
    await page.click('#EnableReminder-yes', {clickCount:1});
    await page.$eval('input[type="submit"]', el => el.click());
    } catch (e) {
        console.log(e);
    }finally {
        await page.close();
        await browser.close();
    }
}) ()

async function initiateCaptchaRequest(apiKey) {
    const formData = {
      method: 'userrecaptcha',
      googlekey: config.sitekey,
      key: config.apiKey,
      pageurl: config.pageurl,
      json: 1
    };
    console.log(`Submitting solution request to 2captcha for ${config.pageurl}`);
    const response = await request.post('http://2captcha.com/in.php', {form: formData});
    return JSON.parse(response).request;
  }
  
  async function pollForRequestResults(key, id, retries = 30, interval = 1500, delay = 15000) {
    console.log(`Waiting for ${delay} milliseconds...`);
    await timeout(delay);
    return poll({
      taskFn: requestCaptchaResults(key, id),
      interval,
      retries
    });
  }
  
  function requestCaptchaResults(apiKey, requestId) {
    const url = `http://2captcha.com/res.php?key=${apiKey}&action=get&id=${requestId}&json=1`;
    return async function() {
      return new Promise(async function(resolve, reject){
          console.log(`Polling for respose...`);
        const rawResponse = await request.get(url);
        const resp = JSON.parse(rawResponse);
        console.log(resp);
        if (resp.status === 0) return reject(resp.request);
        console.log(`Reponse received.`);
        resolve(resp.request);
      });
    }
  }

const timeout = ms => new Promise(res => setTimeout(res, ms))

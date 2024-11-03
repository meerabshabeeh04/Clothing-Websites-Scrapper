// const puppeteer = require("puppeteer");

// const scrape = async () => {
//     const browser = await puppeteer.launch({ headless: false }); // Set to true for headless mode
//     const page = await browser.newPage();

//     const url = "https://laam.pk/nodes/women-kurta-set-181?brand=6teen,a%26j,aahang,aasme+asma,abaan+zohan,abeeha+mishcah,abbas+jamil+rajpoot,abeera,abeera+usman,adam%27s+couture";
//     await page.goto(url, { waitUntil: "networkidle2" });

//     // Wait for the images to load
//     await page.waitForSelector(".image-box img");

//     // Extract image links
//     const newImageLinks = await page.evaluate(() => {
//         const suitElements = document.querySelectorAll(".image-box img");
//         return Array.from(suitElements).map((suit) => suit.getAttribute("src"));
//     });

//     console.log(newImageLinks.length); // Outputs all image URLs

//     await browser.close();
// };

// scrape();

// const puppeteer = require("puppeteer");

// const scrape = async () => {
//     const browser = await puppeteer.launch({ headless: false });
//     const page = await browser.newPage();

//     const url = "https://laam.pk/nodes/women-kurta-set-181?brand=6teen,a%26j,aahang,aasme+asma,abaan+zohan,abeeha+mishcah,abbas+jamil+rajpoot,abeera,abeera+usman,adam%27s+couture";
//     await page.goto(url, { waitUntil: "networkidle2" });

//     // Custom wait function
//     const waitForTimeout = (ms) => new Promise(resolve => setTimeout(resolve, ms));

//     // Scroll and load more content
//     const scrollAndLoadMore = async () => {
//         let previousHeight = 0;
//         let currentHeight = await page.evaluate(() => document.body.scrollHeight);
//         let attempts = 0; // Number of scroll attempts
//         const maxAttempts = 10; // Maximum attempts before stopping

//         while (attempts < maxAttempts) {
//             // Scroll to the bottom of the page
//             await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));

//             // Wait for additional content to load
//             await waitForTimeout(3000); // Increase timeout if necessary

//             // Update the new height after content loads
//             currentHeight = await page.evaluate(() => document.body.scrollHeight);
            
//             if (previousHeight === currentHeight) {
//                 attempts++;
//             } else {
//                 attempts = 0; // Reset attempts if new content loaded
//             }
//             previousHeight = currentHeight;
//         }
//     };

//     await scrollAndLoadMore(); // Trigger infinite scrolling to load all images

//     // Extract image links
//     const newImageLinks = await page.evaluate(() => {
//         const suitElements = document.querySelectorAll(".image-box img");
        
//         return Array.from(suitElements).map((suit) => {
//             // Prefer the srcset attribute, otherwise fallback to src
//             return suit.getAttribute("srcset") || suit.getAttribute("src");
//         }).filter(src => src);  // Filter out any null or empty values
//     });

//     console.log(newImageLinks.length); // Output the number of images found
//     console.log(newImageLinks); // Output the image URLs

//     await browser.close();
// };

// scrape();



// const puppeteer = require("puppeteer");
// const fs = require("fs");
// const path = require("path");
// const axios = require("axios");

// const scrape = async () => {
//     const browser = await puppeteer.launch({ headless: false });
//     const page = await browser.newPage();

//     const url = "https://laam.pk/nodes/women-kurta-set-181?brand=6teen,a%26j,aahang,aasme+asma,abaan+zohan,abeeha+mishcah,abbas+jamil+rajpoot,abeera,abeera+usman,adam%27s+couture";
//     await page.goto(url, { waitUntil: "networkidle2" });

//     const waitForTimeout = (ms) => new Promise(resolve => setTimeout(resolve, ms));

//     const scrollAndLoadMore = async () => {
//         let previousHeight = 0;
//         let currentHeight = await page.evaluate(() => document.body.scrollHeight);
//         let attempts = 0;
//         const maxAttempts = 10;

//         while (attempts < maxAttempts) {
//             await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
//             await waitForTimeout(3000);
//             currentHeight = await page.evaluate(() => document.body.scrollHeight);

//             if (previousHeight === currentHeight) {
//                 attempts++;
//             } else {
//                 attempts = 0; 
//             }
//             previousHeight = currentHeight;
//         }
//     };

//     await scrollAndLoadMore();

//     const newImageLinks = await page.evaluate(() => {
//         const suitElements = document.querySelectorAll(".image-box img");
//         return Array.from(suitElements).map((suit) => {
//             return suit.getAttribute("srcset") || suit.getAttribute("src");
//         }).filter(src => src);
//     });

//     console.log(`Found ${newImageLinks.length} images.`);

//     // Create images directory if it doesn't exist
//     const imagesDir = path.join(__dirname, "imagess");
//     if (!fs.existsSync(imagesDir)) {
//         fs.mkdirSync(imagesDir);
//     }

//     // Download images
//     for (let i = 0; i < newImageLinks.length; i++) {
//         const imageUrl = newImageLinks[i];
//         const fileName = `image_${i + 1}.jpg`; // Name the files as image_1, image_2, etc.
//         const filePath = path.join(imagesDir, fileName);

//         try {
//             const response = await axios({
//                 method: 'get',
//                 url: imageUrl,
//                 responseType: 'stream'
//             });
//             response.data.pipe(fs.createWriteStream(filePath));
//             console.log(`Downloaded: ${fileName}`);
//         } catch (error) {
//             console.error(`Failed to download ${fileName}:`, error.message);
//         }
//     }

//     await browser.close();
// };

// scrape();





const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");
const axios = require("axios");

const MAX_RETRIES = 3; // Number of retries for downloading an image

const scrape = async () => {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    const url = "https://laam.pk/nodes/women-kurta-set-181?brand=renee,sadia+aamir,saffron,saleenz,sana+safinaz,sanaya,sapphire,shahzeb+saeed,shanaya,taanka+official,tania+malik+studio,tassels,the+be+you+official,the+pinktree+company,unaiza+mir,urge+pret,usman+kashif";
    await page.goto(url, { waitUntil: "networkidle2" });

    await page.waitForSelector(".image-box img");

    const scrollAndLoadMore = async () => {
        let previousHeight;
        while (true) {
            previousHeight = await page.evaluate('document.body.scrollHeight');
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)');

            // Use a Promise-based timeout
            await new Promise((resolve) => setTimeout(resolve, 2000)); // Adjust the timeout as necessary

            const newHeight = await page.evaluate('document.body.scrollHeight');
            if (newHeight === previousHeight) break;
        }
    };

    await scrollAndLoadMore();

    const newImageLinks = await page.evaluate(() => {
        const suitElements = document.querySelectorAll(".image-box img");
        return Array.from(suitElements).map((suit) => suit.getAttribute("src"));
    });

    console.log(`Total images found: ${newImageLinks.length}`);

    const downloadImages = async (imageLinks) => {
        const imagesDir = path.join(__dirname, "imagess");
        if (!fs.existsSync(imagesDir)) {
            fs.mkdirSync(imagesDir);
        }

        const downloadWithRetries = async (imageUrl, index) => {
            const fileName = `images20_${index + 1}.jpg`;
            const filePath = path.join(imagesDir, fileName);
            let attempt = 0;

            while (attempt < MAX_RETRIES) {
                try {
                    const response = await axios({
                        method: 'get',
                        url: imageUrl,
                        responseType: 'stream'
                    });
                    response.data.pipe(fs.createWriteStream(filePath));
                    console.log(`Downloading: ${fileName}`);
                    await new Promise((resolve) => response.data.on('end', resolve)); // Wait for the stream to finish
                    return; // Exit the retry loop if successful
                } catch (error) {
                    attempt++;
                    console.error(`Failed to download ${fileName} (Attempt ${attempt}):`, error.message);
                    if (attempt === MAX_RETRIES) {
                        console.error(`Max retries reached for ${fileName}. Skipping...`);
                    }
                }
            }
        };

        const downloadPromises = imageLinks.map((imageUrl, index) => downloadWithRetries(imageUrl, index));

        await Promise.all(downloadPromises);
    };

    await downloadImages(newImageLinks);

    await browser.close();
};

scrape();

/* eslint-disable no-unused-vars */

import fs from "fs";
import { readFile } from "fs/promises";
import path from "path";
import fetch from "node-fetch";

// const body = JSON.parse(await readFile(new URL("./req.json", import.meta.url)));
const reqTmpl = JSON.parse(
  await readFile(new URL("./req-tmpl.json", import.meta.url))
);
// // https://www.stefanjudis.com/snippets/how-to-import-json-files-in-es-modules-node-js/
// const buckets = JSON.parse(
//   await readFile(
//     new URL("./ds/getsiteprofile/2022-10-21T11.json", import.meta.url)
//   )
// );

const Default_Headers = {
  "Content-Type": "application/json; charset=UTF-8",
  "Accept-Encoding": "gzip, deflate",
  "kbn-xsrf": "kibana",
};
const Kibana_URL = "";
const Path_Param = encodeURIComponent("prd-narra.request-2022.10.*/_search");
const Path_Param_Scroll = encodeURIComponent(
  "prd-narra.request-2022.10.*/_search?scroll=2m"
);
const Scroll_Param = encodeURIComponent("/_search/scroll");

async function waitFor(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve(), ms);
  });
}

function save(dir, name, data) {
  let fullDir = path.resolve("ds", dir);
  if (!fs.existsSync(fullDir)) {
    fs.mkdirSync(fullDir);
  }
  let file = `${fullDir}/${name}.json`;
  fs.writeFile(file, data, (err) => {
    if (err) {
      console.error(err);
    }

    console.log(`${file} saved.`);
  });
}

function getFilter(api, dateRange) {
  let filter = [
    {
      match_phrase: {
        "j.URL": api,
      },
    },
    {
      range: {
        "@timestamp": {
          format: "strict_date_optional_time",
          gte: dateRange[0],
          lte: dateRange[1],
        },
      },
    },
  ];

  return filter;
}

function parse(buckets) {
  console.debug(`will process ${buckets.length} records.`);

  const arr = [];
  for (const it of buckets) {
    let bkt = it["1"].buckets;
    // console.debug(
    //   `${it.key}: total count ${it.doc_count}, time frame ${bkt.length}`
    // );

    for (const ib of bkt) {
      // console.debug(`${new Date(ib.key).toLocaleString()}: ${ib.doc_count}`);
      let obj = { ip: it.key };
      obj["ts"] = ib.key;
      obj["c"] = ib.doc_count;
      arr.push(obj);
    }
  }

  return arr;
}

async function getSearchAfter() {}
async function getScroll(scroll_id) {
  // ?path=%2F_search%2Fscroll&method=POST
  const url = `${Kibana_URL}?path=${Scroll_Param}&method=POST`;
  const body = {
    scroll: "1m",
    scroll_id,
  };

  const response = await fetch(url, {
    method: "POST",
    body: JSON.stringify(body),
    headers: Default_Headers,
  });
  const data = await response.json();

  console.debug(data);
}
async function getSearch(name, api, dateRange) {
  const url = `${Kibana_URL}?path=${Path_Param}&method=GET`;
  const body = reqTmpl;
  body.query.bool.filter = getFilter(api, dateRange);
  // console.debug(JSON.stringify(body));

  const response = await fetch(url, {
    method: "POST",
    body: JSON.stringify(body),
    headers: Default_Headers,
  }).catch((err) => console.error(err));
  const data = await response.json();

  if (data._scroll_id) {
    getScroll(data._scroll_id);
  }

  console.debug(data);
  const buckets = data.aggregations["0"].buckets;
  if (buckets.length > 0) {
    save(api.split("/").pop(), name, JSON.stringify(parse(buckets)));
  }
}
async function retrieveForApi(api) {
  let dates = [21, 22, 23, 28, 29, 30];
  let times = [19, 20, 21, 22, 23, 24];

  for (const d of dates) {
    for (let index = 0; index < times.length - 1; index++) {
      let start = new Date(2022, 9, d, times[index]).toISOString();
      let end = new Date(2022, 9, d, times[index + 1]).toISOString();
      let file = start.substring(0, 13);
      console.debug(`${file} , ${start} ~ ${end}`);

      console.debug("start");
      await getSearch(file, api, [start, end]);

      await waitFor(Math.floor(Math.random() * 10) * 1000);
      console.debug("end.");
    }
  }
}

(async function () {
  const ApiGroups = [
    [
      "/home/getsiteprofile",
      "/event/getsportevents",
      "/event/getallliveevents",
      "/event/getfavouriteevents",
      "/event/getfavouriteeventscount",
      "/event/getpopulareventlist",
      "/member/getmemberbalance",
      "/placebet/getbetinfo",
      "/mybet/getbetlist",
      "/result/getliveresult",
      "/mybet/getbetstatement",
    ],
    [
      "/announcement/getannouncement",
      "/announcement/getpa",
      "/announcement/getpaind",
      "/announcement/getscrollingannouncement",
      "/announcement/updatepa",
      "/event/addfavouriteevents",
      "/event/getalllivesportmenu",
      "/event/getcompetitionlist",
      "/event/geteventbyids",
      "/event/geteventselections",
      "/event/gethomelive",
      "/event/gethomepopular",
    ],
    [
      "/event/gethomeupcoming",
      "/event/getlivecenter",
      "/event/getorevents",
      "/event/getoutrightbycompetition",
      "/event/getoutrighteventbyeventids",
      "/event/getparticipantlist",
      "/event/getpopularsportmenu",
      "/event/getselectleague",
      "/event/getsporteventsbymarket",
      "/event/getupcomingeventlist",
      "/event/getupcomingsportmenu",
    ],
    [
      "/event/getvseventdetails",
      "/event/getvseventinfo",
      "/event/loglivestreamrequest",
      "/event/removefavouriteevents",
      "/home/getcyberbattlemenu",
      "/home/gethomemenusportcount",
      "/home/gethomemenusportcountbycompetition",
      "/home/getleftpanelsportcount",
      "/home/getserverdatetime",
      "/home/getsportcountbysportid",
      "/home/logmessage",
    ],
    [
      "/home/logvidtogb",
      "/member/getmemberpreferences",
      "/member/logout",
      "/member/updatefavouritesport",
      "/member/updatememberpreferences",
      "/mybet/clearpendingrejectedcount",
      "/mybet/getaledformb",
      "/mybet/getallliveeventsformybet",
      "/mybet/getlatestbuybackinfo",
      "/mybet/getpendingrejectedcount",
      "/mybet/getwagerinfobywagerid",
    ],
    [
      "/mybet/submitbuyback",
      "/placebet/comboplacebet",
      "/placebet/getpendingwagerstatus",
      "/placebet/getrs",
      "/placebet/singleplacebet",
      "/promotion/getpromotionslist",
      "/result/getcompletedresultlist",
      "/result/getoutrightresultlist",
      "/search/getrecentpopularsearch",
      "/search/getsearchall",
      "/search/getsearchresultsgroupbysport",
      "/search/updaterecentsearch",
    ],
  ];

  // console.log('total numbers: ', ApiGroups.reduce((prev, curr) => prev + curr.length, 0));
  // for (const g of ApiGroups) {
  //   console.log("--------------");
  //   console.log(g);
  //   console.log(g.length);
  // }

  // // run by batch
  // for (const api of ApiGroups[0]) {
  //   await retrieveForApi(api);
  // }
})();

// testing

// parse(buckets);

// // special testing
// getSearch("test", "/home/getsiteprofile", [
//   "2022-10-28T12:00:00.000Z",
//   "2022-10-28T13:00:00.000Z",
// ]);

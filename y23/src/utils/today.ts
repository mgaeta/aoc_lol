import { DateTime } from "luxon";

const currentTime = DateTime.now().setZone("America/New_York");

export const currentYear = currentTime.year.toString();

export const todayRaw = currentTime.day.toString();

export const today = todayRaw.padStart(2, "0");

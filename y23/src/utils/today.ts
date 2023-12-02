import { DateTime } from "luxon";

export const today = DateTime.now().setZone("America/New_York").day.toString().padStart(2, "0");

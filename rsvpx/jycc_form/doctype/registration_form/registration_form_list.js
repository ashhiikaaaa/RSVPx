frappe.listview_settings["Hotel Registration"] = {
    get_indicator(doc) {

        if (
            doc.status === "Conflict" ||
            doc.status === "Partner Already Requested" ||
            doc.status === "Partner Chose Someone Else"
        ) {
            return [doc.status, "red"];
        }

        if (doc.status === "Matched") {
            return [doc.status, "green"];
        }

        return [doc.status, "orange"];
    }
};
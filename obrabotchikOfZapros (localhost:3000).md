obrabotchikOfZapros (localhost:3000)
    ADDRESS check
        /raids
            METHOD check
                GET
                    -> DO SOMETHING
                POST
                    -> DO SOMETHING
                PUT
                    -> DO SOMETHING
                DELETE
                    -> DO SOMETHING
        /characters
        /characters/:id
                GET
                    ->
                        getall raids data
                        remember total number of raids
                        get number of attendance
                        get total attendance
                        get items list for characters

                        return {
                            items:[...]
                            attendance: number
                            attendancePercent: number
                        }
                    -> DO SOMETHING
                POST
                    Add character to character table
        /guild
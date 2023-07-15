// Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
// Licensed under the Amazon Software License  http://aws.amazon.com/asl/

import React from "react";
import { DocumentForInf } from "../../../utils/interface";
import { Link } from "@chakra-ui/react";

export default class QuotedTexts extends React.Component<{ fulltext: string, contexts: DocumentForInf[] }, {}> {
    // 引用にリンクを付与する


    render() {
        const { fulltext, contexts } = this.props;

        let pivot: number = 0;

        return (
            <span>
                {
                    [...fulltext].map((t, ti) => (
                        (() => {
                            if (t === "[" && ti !== 0) {
                                let component = <span key={ti}>{fulltext.substring(pivot, ti)}</span>
                                pivot = ti
                                return (component)
                            } else if (t === "]") {
                                let url = ""
                                let contextId = Number(fulltext.substring(pivot + 1, ti));
                                if (contexts[contextId]) {
                                    url = contexts[contextId].content
                                }
                                let component = <span key={ti}><Link color="green.500" href={url} isExternal>{fulltext.substring(pivot, ti + 1)}</Link></span>
                                pivot = ti + 1
                                return (component)
                            }
                        })()
                    )
                    )
                }
                <span>{fulltext.substring(pivot, fulltext.length)}</span>
            </span>
        )
    }
}
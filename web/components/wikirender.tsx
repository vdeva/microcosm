"use client";

import wtf from "wtf_wikipedia";
// @ts-ignore
import wtfPluginHtml from "wtf-plugin-html";
wtf.extend(wtfPluginHtml);

import "@/styles/wiki.css";

export function WikiRender(props: { contents: string }) {
  wtf;

  return (
    // @ts-ignore
    <div dangerouslySetInnerHTML={{ __html: wtf(props.contents).html() }} />
  );
}

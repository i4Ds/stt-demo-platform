import { Injectable } from '@angular/core';
import {environment} from "../../environments/environment";

declare global {
  interface Window {
    _paq: any;
  }
}

function initMatomo() {
  if (environment.matomoUrl) {
    const _paq = window._paq = window._paq || [];
    /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
    _paq.push(['trackPageView']);
    _paq.push(['enableLinkTracking']);
    _paq.push(['setTrackerUrl', environment.matomoUrl+'matomo.php']);
    _paq.push(['setSiteId', '1']);
    const d = document, g = d.createElement('script'), s = d.getElementsByTagName('script')[0];
    g.async=true;
    g.src=environment.matomoUrl+'matomo.js';
    s.parentNode?.insertBefore(g,s);
  }
}

@Injectable({
  providedIn: 'root'
})
export class MatomoService {
  constructor() {
    initMatomo();
  }

  getVisitorId(): Promise<string> {
    return new Promise<string>((resolve, reject) => {
      if(window._paq) {
        window._paq.push([function (this: any) {resolve(this.getVisitorId())}]);
      } else {
        reject();
      }
    });
  }

  trackEvent(category: string, action: string, name: string, value: number|null = null) {
    if(window._paq) {
      if (value !== null) {
        window._paq.push(['trackEvent', category, action, name, value]);
      } else {
        window._paq.push(['trackEvent', category, action, name]);
      }
    }
  }
}


import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Subject } from 'rxjs';

export interface SystemState {
  status: string;
  detail: string;
  vitals: {
    cpu_percent: number;
    ram_percent: number;
    neural_activity: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class VenomService {
  private socket: WebSocket | null = null;
  public state$ = new Subject<SystemState>();

  constructor(private http: HttpClient) {
    this.connect();
  }

  private connect() {
    const protocol = globalThis.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = globalThis.location.hostname;
    // If we're on port 4200 (Angular dev server), point to 8000 (FastAPI)
    const port = globalThis.location.port === '4200' ? '8000' : globalThis.location.port;
    const wsUrl = `${protocol}//${host}:${port}/ws/system-stream`;

    console.log('Connecting to Neural Link:', wsUrl);

    this.socket = new WebSocket(wsUrl);
    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.state$.next(data);
      } catch (e) {
        console.error('Telepathic interference:', e);
      }
    };
    this.socket.onclose = () => {
      console.warn('Neural link severed. reconnecting...');
      setTimeout(() => this.connect(), 2000);
    };
  }

  sendCommand(text: string) {
    const host = globalThis.location.hostname;
    const port = globalThis.location.port === '4200' ? '8000' : globalThis.location.port;
    const apiUrl = `${globalThis.location.protocol}//${host}:${port}/api/command`;
    return this.http.post(apiUrl, { text }).subscribe();
  }
}

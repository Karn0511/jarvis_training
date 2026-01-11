
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { VenomService, SystemState } from './venom.service';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  state: SystemState = {
    status: 'BOOTING',
    detail: 'Initializing Symbiotic Link...',
    vitals: { cpu_percent: 0, ram_percent: 0, neural_activity: 0 }
  };
  history: string[] = [];
  commandInput: string = '';
  connectionLines: any[] = [];
  recentActivities: any[] = [
    { text: 'Neural Cascade Phase 4: Synchronized', color: '#d4af37' },
    { text: 'Quantum Core Temperature: Nominal', color: '#94a3b8' },
    { text: 'Symbiotic Link Encryption: Active', color: '#0f172a' },
    { text: 'Heuristic Pattern Matched: 0.998', color: '#d4af37' }
  ];
  startTime = Date.now();

  constructor(private venom: VenomService) {}

  getRandomPos(): number {
    return Math.random() * 80 + 10;
  }

  getTimestamp(): string {
    const now = new Date();
    return `[${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}]`;
  }

  getUptime(): string {
    const seconds = Math.floor((Date.now() - this.startTime) / 1000);
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours}h ${mins}m ${secs}s`;
  }

  quickCommand(cmd: string): void {
    this.commandInput = cmd;
    this.submitCommand();
  }

  ngOnInit() {
    this.venom.state$.subscribe((data: SystemState) => {
      this.state = data;
      if (data.detail && (this.history.length === 0 || this.history[0] !== data.detail)) {
        this.history.unshift(data.detail);
        if (this.history.length > 20) this.history.pop();
      }
    });
  }

  get statusColor(): string {
    const colors: Record<string, string> = {
      'THINKING': '#d4af37',
      'LISTENING': '#94a3b8',
      'PROCESSING': '#0f172a',
      'ERROR': '#ef4444',
      'OFFLINE': '#334155'
    };
    return colors[this.state.status] || '#d4af37';
  }

  submitCommand() {
    if (this.commandInput.trim()) {
      this.venom.sendCommand(this.commandInput);
      this.commandInput = '';
    }
  }
}

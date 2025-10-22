// Application constants
export const APP_CONFIG = {
    NAME: 'JobApp Automator',
    DESCRIPTION: 'AI-powered job application automation for South Africa',
    VERSION: '1.0.0',
    SERVICE_FEE: 499.00,
    CURRENCY: 'ZAR',
};

// South African regions and towns
export const REGIONS = {
    gauteng: [
        'Johannesburg', 'Pretoria', 'Sandton', 'Randburg', 'Roodepoort',
        'Centurion', 'Midrand', 'Alberton', 'Kempton Park', 'Boksburg',
        'Benoni', 'Springs', 'Vereeniging', 'Vanderbijlpark'
    ],
    western_cape: [
        'Cape Town', 'Stellenbosch', 'Paarl', 'Wellington', 'George',
        'Mossel Bay', 'Worcester', 'Malmesbury', 'Bellville', 'Parow',
        'Somerset West', 'Constantia'
    ],
    eastern_cape: [
        'Port Elizabeth', 'East London', 'Grahamstown', 'Queenstown',
        'Bisho', 'Butterworth', 'Uitenhage', 'Graaff-Reinet'
    ],
    kwaZulu_natal: [
        'Durban', 'Pietermaritzburg', 'Richards Bay', 'Newcastle',
        'Ladysmith', 'Ballito', 'Umhlanga', 'Pinetown'
    ],
    free_state: [
        'Bloemfontein', 'Welkom', 'Bethlehem', 'Kroonstad', 'Sasolburg',
        'Phuthaditjhaba', 'Botshabelo'
    ],
    limpopo: [
        'Polokwane', 'Lebowakgomo', 'Tzaneen', 'Phalaborwa', 'Modimolle',
        'Bela-Bela', 'Mokopane'
    ],
    mpumalanga: [
        'Nelspruit', 'Witbank', 'Middelburg', 'Standerton', 'Ermelo',
        'Bushbuckridge', 'Mbombela'
    ],
    north_west: [
        'Rustenburg', 'Potchefstroom', 'Klerksdorp', 'Mahikeng', 'Zeerust',
        'Lichtenburg', 'Stilfontein'
    ],
    northern_cape: [
        'Kimberley', 'Upington', 'Springbok', 'De Aar', 'Kuruman',
        'Postmasburg', 'Kathu'
    ]
};

// Job industries
export const INDUSTRIES = [
    'Accounting & Finance',
    'Administration',
    'Agriculture',
    'Banking & Insurance',
    'Construction',
    'Customer Service',
    'Education & Training',
    'Engineering',
    'Healthcare',
    'Hospitality & Tourism',
    'Human Resources',
    'IT & Technology',
    'Legal',
    'Manufacturing',
    'Marketing & Communications',
    'Mining',
    'Real Estate',
    'Retail',
    'Sales',
    'Transport & Logistics',
    'Other'
];

// Job types
export const JOB_TYPES = [
    'Full-time',
    'Part-time',
    'Contract',
    'Temporary',
    'Remote',
    'Hybrid'
];

// Experience levels
export const EXPERIENCE_LEVELS = [
    'Entry Level',
    'Junior',
    'Mid Level',
    'Senior',
    'Executive'
];

// File upload configurations
export const FILE_CONFIG = {
    MAX_SIZE: 16 * 1024 * 1024, // 16MB
    ALLOWED_EXTENSIONS: ['.pdf', '.doc', '.docx', '.txt'],
    ALLOWED_MIME_TYPES: [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain'
    ]
};

// Payment methods
export const PAYMENT_METHODS = {
    PAYFAST: 'payfast',
    EFT: 'eft'
};

// Application statuses
export const APPLICATION_STATUS = {
    PENDING: 'pending',
    PROCESSING: 'processing',
    COMPLETED: 'completed',
    FAILED: 'failed'
};

// API endpoints
export const API_ENDPOINTS = {
    AUTH: {
        LOGIN: '/api/auth/login',
        REGISTER: '/api/auth/register',
        PROFILE: '/api/auth/profile',
        CHANGE_PASSWORD: '/api/auth/change-password'
    },
    PAYMENTS: {
        INITIATE: '/api/payments/initiate',
        STATUS: '/api/payments/status'
    },
    APPLICATIONS: {
        CREATE: '/api/applications/create',
        PROCESS: '/api/applications/process',
        HISTORY: '/api/applications/history',
        REGIONS: '/api/applications/regions'
    },
    AI: {
        ENHANCE_RESUME: '/api/ai/enhance-resume',
        GENERATE_COVER_LETTER: '/api/ai/generate-cover-letter',
        OPTIMIZE_ATS: '/api/ai/optimize-ats',
        PROCESS_DOCUMENT: '/api/ai/process-document',
        ANALYZE_JOB_DESCRIPTION: '/api/ai/analyze-job-description'
    }
};

// Local storage keys
export const STORAGE_KEYS = {
    AUTH_TOKEN: 'token',
    USER_DATA: 'user_data',
    PAYMENT_DATA: 'payment_data'
};

// Route paths
export const ROUTES = {
    HOME: '/',
    LOGIN: '/login',
    REGISTER: '/register',
    DASHBOARD: '/dashboard',
    APPLICATIONS: '/applications',
    PROFILE: '/profile',
    PAYMENT: '/payment',
    PAYMENT_SUCCESS: '/payment/success',
    PAYMENT_CANCEL: '/payment/cancel'
};

// Theme colors
export const COLORS = {
    primary: {
        50: '#eff6ff',
        100: '#dbeafe',
        200: '#bfdbfe',
        300: '#93c5fd',
        400: '#60a5fa',
        500: '#3b82f6',
        600: '#2563eb',
        700: '#1d4ed8',
        800: '#1e40af',
        900: '#1e3a8a'
    },
    success: {
        50: '#f0fdf4',
        100: '#dcfce7',
        200: '#bbf7d0',
        300: '#86efac',
        400: '#4ade80',
        500: '#22c55e',
        600: '#16a34a',
        700: '#15803d',
        800: '#166534',
        900: '#14532d'
    },
    warning: {
        50: '#fffbeb',
        100: '#fef3c7',
        200: '#fde68a',
        300: '#fcd34d',
        400: '#fbbf24',
        500: '#f59e0b',
        600: '#d97706',
        700: '#b45309',
        800: '#92400e',
        900: '#78350f'
    },
    error: {
        50: '#fef2f2',
        100: '#fee2e2',
        200: '#fecaca',
        300: '#fca5a5',
        400: '#f87171',
        500: '#ef4444',
        600: '#dc2626',
        700: '#b91c1c',
        800: '#991b1b',
        900: '#7f1d1d'
    }
};

export default {
    APP_CONFIG,
    REGIONS,
    INDUSTRIES,
    JOB_TYPES,
    EXPERIENCE_LEVELS,
    FILE_CONFIG,
    PAYMENT_METHODS,
    APPLICATION_STATUS,
    API_ENDPOINTS,
    STORAGE_KEYS,
    ROUTES,
    COLORS
};
